import datetime
from django.core.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.accounts.permissions.IsOwnerOrAdmin import IsOwnerOrAdmin
from apps.accounts.permissions.IsBooker import IsBooker
from apps.booking.models.Booking import Booking
from apps.booking.serializers.booking import BookingSerializer, ReadBookingSerializer
from apps.accounts.exceptions import PrivilegeError
from apps.util import utils
from apps.system_administration.models.system_settings import SystemSettings


class BookingList(ListAPIView):
    permission_classes = ()
    serializer_class = ReadBookingSerializer
    queryset = Booking.objects.all()

    def get_queryset(self):
        qs = super(BookingList, self).get_queryset()

        # Filter by year
        year = self.request.GET.get('year')
        if year:
            qs = qs.filter(date__year=year)

        # Filter by month
        month = self.request.GET.get('month')
        if month:
            qs = qs.filter(date__month=month)

        # Filter by day
        day = self.request.GET.get('day')
        if day:
            qs = qs.filter(date__day=day)

        return qs


class BookingCreate(APIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = BookingSerializer

    def post(self, request):
        data = request.data
        data["booker"] = request.user.id

        if not request.user.is_superuser:
            data["bypass_privileges"] = False

        serializer = BookingSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = serializer.save()
            booking.merge_with_neighbouring_bookings()
            booking.save()
            utils.log_model_change(booking, utils.ADDITION, request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ValidationError, PrivilegeError) as error:
            return Response(error.message, status=status.HTTP_400_BAD_REQUEST)


class BookingRetrieveUpdateDestroy(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin, IsBooker)
    serializer_class = BookingSerializer

    def patch(self, request, pk):

        try:
            booking = Booking.objects.get(id=pk)
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check user permissions
        self.check_object_permissions(request, booking.booker)

        # Check if Booking started.
        now = datetime.datetime.now()

        settings = SystemSettings.get_settings()
        timeout = (now + settings.booking_edit_lock_timeout).time()

        if now.date() > booking.date or (now.date() == booking.date and timeout >= booking.start_time):
            return Response("Can't modify booking anymore.", status=status.HTTP_403_FORBIDDEN)

        data = request.data
        data["booker"] = booking.booker.id

        if "bypass_privileges" in data and not request.user.is_superuser:
            del data["bypass_privileges"]

        serializer = BookingSerializer(booking, data=data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            update_booking = serializer.save()

            utils.log_model_change(update_booking, utils.CHANGE, request.user)

            update_booking.merge_with_neighbouring_bookings()
            update_booking.save()

            utils.log_model_change(update_booking, utils.CHANGE, request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)
