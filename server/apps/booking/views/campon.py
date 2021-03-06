import datetime
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.exceptions import PrivilegeError
from apps.accounts.permissions.IsBooker import IsBooker
from apps.accounts.permissions.IsOwnerOrAdmin import IsOwnerOrAdmin
from apps.booking.models.CampOn import CampOn
from apps.booking.models.Booking import Booking
from apps.booker_settings.models.EmailSettings import EmailSettings
from apps.booking.serializers.campon import CampOnSerializer, ReadCampOnSerializer
from apps.booking.serializers.booking import BookingSerializer
from apps.util import utils


class CampOnList(ListAPIView):
    permission_classes = ()
    serializer_class = ReadCampOnSerializer
    queryset = CampOn.objects.all()

    def get_queryset(self):
        qs = super(CampOnList, self).get_queryset()

        try:
            # Filter by id
            id = self.request.GET.get('id')
            if id:
                qs = CampOn.objects.filter(id=id)

            # Filter by booking_id
            booking_id = self.request.GET.get('booking_id')
            if booking_id:
                qs = CampOn.objects.filter(camped_on_booking__id=booking_id)

            # Filter by start_time
            start_time = self.request.GET.get('start_time')
            if start_time:
                qs = CampOn.objects.filter(start_time=start_time)

            # Filter by end_time
            end_time = self.request.GET.get('end_time')
            if end_time:
                qs = CampOn.objects.filter(end_time=end_time)

            # Filter by year
            year = self.request.GET.get('year')
            if year:
                qs = qs.filter(camped_on_booking__date__year=year)

            # Filter by month
            month = self.request.GET.get('month')
            if month:
                qs = qs.filter(camped_on_booking__date__month=month)

            # Filter by day
            day = self.request.GET.get('day')
            if day:
                qs = qs.filter(camped_on_booking__date__day=day)
        except Exception:
            raise APIException

        return qs


class CampOnCreate(APIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = CampOnSerializer

    def post(self, request):

        data = request.data
        data["booker"] = request.user.id

        # Rounding to nearest 10th minute, as bookings and camp-ons can only be made every ten minute interval
        time = utils.get_rounded_time(10)

        data["start_time"] = time.time()
        serializer = CampOnSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Looking for booking to camp onto in the database, returning if not found
        try:
            current_booking = Booking.objects.get(id=data["camped_on_booking"])
            request_end_time = datetime.datetime.strptime(data["end_time"], "%H:%M").time()
        except Booking.DoesNotExist:
            return Response("No Booking to camp on to", status=status.HTTP_400_BAD_REQUEST)

        if current_booking.booker.username == request.user.username:
            return Response("You can't camp on to your own booking", status=status.HTTP_401_UNAUTHORIZED)

        # If the camp on doesn't end later than the booking, then we create the camp on
        # Otherwise we will attempt to create a booking following the camp on
        if request_end_time <= current_booking.end_time:
            try:
                camp_on = serializer.save()
                utils.log_model_change(camp_on, utils.ADDITION, request.user)
                return Response({"CampOn": CampOnSerializer(camp_on).data}, status=status.HTTP_201_CREATED)
            except ValidationError as error:
                return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)

        # Checking if there are bookings in the time period between the end of the booking and the end of the camp on
        # This is done on top of the model validation, as we will need to save a camp on and a booking at the same time
        bookings = Booking.objects.filter(
            start_time__gte=current_booking.end_time,
            start_time__lt=request_end_time,
            room=current_booking.room
        )

        if bookings:
            return Response("End time overlaps with future booking", status=status.HTTP_409_CONFLICT)

        # No Booking found, create new Booking and create CampOn
        data["end_time"] = current_booking.end_time
        new_camp_on_serializer = CampOnSerializer(data=data)

        if not new_camp_on_serializer.is_valid():
            return Response(new_camp_on_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Creation of the camp on and the generated booking
        # If there is a privilege error for the booking (user already has a maximum amount of bookings)
        # only the camp on will be created
        # May have to be tweaked if we want to cancel the camp on if there is a privilege error
        try:
            camp_on = new_camp_on_serializer.save()
            new_booking = Booking(booker=camp_on.booker,
                                  group=camp_on.camped_on_booking.group,
                                  room=camp_on.camped_on_booking.room,
                                  date=camp_on.camped_on_booking.date,
                                  start_time=camp_on.end_time,
                                  end_time=request_end_time)

            new_booking.save()
            camp_on.generated_booking = new_booking
            camp_on.save()
            utils.log_model_change(camp_on, utils.ADDITION, request.user)
            utils.log_model_change(new_booking, utils.ADDITION, request.user)
        except (PrivilegeError, ValidationError) as error:
            if isinstance(error, PrivilegeError):
                return Response(error.message, status=status.HTTP_403_FORBIDDEN)
            if isinstance(error, ValidationError):
                return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)

        response_data = {"CampOn": CampOnSerializer(camp_on).data,
                         "Booking": BookingSerializer(new_booking).data}
        email_settings = EmailSettings.objects.get_or_create(booker=camp_on.camped_on_booking.booker)[0]
        if email_settings.when_camp_on_booking:
            email_subject = "Camping on your booking!"
            email_message = "Someone made a camp-on on your booking. Make sure you are in the room or you may lose it."
            current_booking.booker.send_email(email_subject, email_message)
        return Response(response_data, status=status.HTTP_201_CREATED)


class CamponCancel(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin, IsBooker)

    def post(self, request, pk):
        try:
            campon = CampOn.objects.get(id=pk)
        except Booking.DoesNotExist:
            return Response("Selected camp on to cancel does not exist", status=status.HTTP_400_BAD_REQUEST)

        is_admin = False
        if request.user.is_superuser:
            is_admin = True

        try:
            id = campon.id
            delete = campon.delete_campon(is_admin)
            if delete:
                campon.id = id
                utils.log_model_change(campon, utils.DELETION, request.user)
            else:
                utils.log_model_change(campon, utils.CHANGE, request.user)
        except ValidationError as error:
            return Response(error.message, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class CamponRetrieveUpdateDestroy(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin, IsBooker)

    def patch(self, request, pk):
        data = request.data

        try:
            campon = CampOn.objects.get(id=pk)
        except Booking.DoesNotExist:
            return Response("Selected camp on to edit does not exist", status=status.HTTP_400_BAD_REQUEST)

        request_end_time = datetime.datetime.strptime(data["end_time"], "%H:%M").time()

        is_admin = False
        if request.user.is_superuser:
            is_admin = True

        try:
            campon.edit(request_end_time, is_admin)
            utils.log_model_change(campon, utils.CHANGE, request.user)
        except ValidationError as error:
            return Response(error.message, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
