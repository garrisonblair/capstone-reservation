import datetime
from django.core.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.permissions.IsBooker import IsBooker
from apps.booking.models.CampOn import CampOn
from apps.booking.models.Booking import Booking
from apps.booking.serializers.campon_serializer import CampOnSerializer
from apps.booking.serializers.booking_serializer import BookingSerializer


class CampOnList(ListAPIView):
    permission_classes = ()
    serializer_class = CampOnSerializer
    queryset = CampOn.objects.all()

    def get_queryset(self):
        qs = super(ListAPIView, self).get_queryset()

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

        return qs

    def get(self, request):
        try:
            qs = self.get_queryset()
            serializer = CampOnSerializer(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)


# TODO: Refactor
class CampOnCreate(APIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = CampOnSerializer

    def post(self, request):

        data = request.data
        data["booker"] = request.user.booker.booker_id

        # Round to nearest 10th minute
        time = datetime.datetime.now().replace(microsecond=0)
        discard = datetime.timedelta(
            minutes=time.minute % 10,
            seconds=time.second,
            microseconds=time.microsecond
        )
        time -= discard
        if discard >= datetime.timedelta(minutes=5):
            time += datetime.timedelta(minutes=10)

        data["start_time"] = time.time()
        serializer = CampOnSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Find current booking to be camped on
            current_booking = Booking.objects.get(id=data["camped_on_booking"])
            request_end_time = datetime.datetime.strptime(data["end_time"], "%H:%M").time()

            # Check if requested end time ends after the current_current end time
            if request_end_time > current_booking.end_time:
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

                camp_on = new_camp_on_serializer.save()

                new_booking = Booking(booker=camp_on.booker,
                                      group=camp_on.camped_on_booking.group,
                                      room=camp_on.camped_on_booking.room,
                                      date=camp_on.camped_on_booking.date,
                                      start_time=camp_on.end_time,
                                      end_time=request_end_time)

                new_booking.save()
                camp_on.generated_booking = new_booking

                response_data = {"CampOn": CampOnSerializer(camp_on).data,
                                 "Booking": BookingSerializer(new_booking).data}
                return Response(response_data, status=status.HTTP_201_CREATED)

            camp_on = serializer.save()
            return Response({"CampOn": CampOnSerializer(camp_on).data}, status=status.HTTP_201_CREATED)

        except (ValueError, ValidationError) as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)
