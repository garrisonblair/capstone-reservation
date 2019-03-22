import datetime
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.permissions.IsBooker import IsBooker
from apps.accounts.permissions.IsOwnerOrAdmin import IsOwnerOrAdmin
from apps.accounts.exceptions import PrivilegeError
from apps.booking.models.RecurringBooking import RecurringBooking
from apps.booking.models.Booking import Booking
from apps.rooms.models.Room import Room
from apps.booking.serializers.recurring_booking import RecurringBookingSerializer
from apps.rooms.serializers.room import RoomSerializer
from apps.util import utils
from datetime import timedelta, datetime
from apps.system_administration.models.system_settings import SystemSettings


class RecurringBookingCreate(APIView):
    permission_classes = (IsAuthenticated, IsBooker)

    def post(self, request):

        recurring_booking_data = request.data
        recurring_booking_data["booker"] = request.user.id

        serializer = RecurringBookingSerializer(data=recurring_booking_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            recurring_booking, conflicts = serializer.create(validated_data=serializer.validated_data)
            utils.log_model_change(recurring_booking,
                                   utils.ADDITION,
                                   request.user)
            for booking in recurring_booking.booking_set.all():
                utils.log_model_change(booking,
                                       utils.ADDITION,
                                       request.user)

            return Response(conflicts, status=status.HTTP_201_CREATED)
        except (ValidationError, PrivilegeError) as error:
            if isinstance(error, PrivilegeError):
                return Response(error.message, status=status.HTTP_401_UNAUTHORIZED)
            elif ((error.message == "Start date can not be after End date.") or
                  (error.message == "You must book for at least two consecutive weeks.") or
                  (error.message == "Start time can not be after End time.")):
                return Response(error.message, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(error.message, status=status.HTTP_409_CONFLICT)


class RecurringBookingCancel(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin, IsBooker)
    serializer_class = RecurringBookingSerializer

    def post(self, request, pk):

        settings = SystemSettings.get_settings()

        # Ensure that recurring booking to be canceled exists
        try:
            recurring_booking = RecurringBooking.objects.get(id=pk)
        except RecurringBooking.DoesNotExist as e:
            return Response('Booking does not exist.', status=status.HTTP_400_BAD_REQUEST)

        # Check user permissions
        self.check_object_permissions(request, recurring_booking.booker)

        # Check if Booking has ended and if it has, disable booking from being canceled
        now = datetime.now()
        today = datetime.today()
        timeout = (now + settings.booking_edit_lock_timeout).time()

        # Checks if current selected recurring booking has started or not yet and handles accordingly
        if now.date() > recurring_booking.end_date \
                or (now.date() == recurring_booking.end_date and timeout >= recurring_booking.end_time):
            if not request.user.is_superuser:
                return Response("Selected booking cannot be canceled as booking has started",
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            # Gets all bookings associated to the indicated booking
            all_associated_booking_instances = recurring_booking.booking_set.all()
            for associated_booking in all_associated_booking_instances:
                # print('(associated_booking.date == today.date
                # and associated_booking.start_time > timeout)', (associated_booking.date == today.date and
                # associated_booking.start_time > timeout))
                # If the date of the recurring booking is after the current indicated booking date, try to delete
                if associated_booking.date > now.date() or (associated_booking.date == today.date()
                                                            and associated_booking.start_time > timeout):
                    associated_booking.delete_booking()
                    utils.log_model_change(recurring_booking, utils.DELETION, request.user)

        except (ValidationError, PrivilegeError) as error:
            if isinstance(error, PrivilegeError):
                return Response(error.message, status=status.HTTP_401_UNAUTHORIZED)
            elif ((error.message == "You must book for at least two consecutive weeks.") or
                  (error.message == "Start time can not be after End time.")):
                return Response(error.message, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(error.message, status=status.HTTP_409_CONFLICT)

        return Response(status=status.HTTP_200_OK)


class RecurringBookingEdit(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin, IsBooker)
    serializer_class = RecurringBookingSerializer

    def post(self, request, pk):

        # Ensure that recurring booking to be modified exists
        try:
            recurring_booking = RecurringBooking.objects.get(id=pk)
        except RecurringBooking.DoesNotExist:
            return Response("Selected booking to edit does not exist", status=status.HTTP_400_BAD_REQUEST)

        # Check user permissions
        self.check_object_permissions(request, recurring_booking.booker)

        data = request.data

        if "skip_conflicts" in data:
            skip_conflicts = data['skip_conflicts']
        else:
            skip_conflicts = False

        if "start_date" in data:
            start_date = data["start_date"]
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        else:
            start_date = None
        if "end_date" in data:
            end_date = data["end_date"]
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            end_date = None
        if "booking_start_time" in data:
            booking_start_time = data["booking_start_time"]
            booking_start_time = datetime.strptime(booking_start_time, '%H:%M:%S').time()
        else:
            booking_start_time = None
        if "booking_end_time" in data:
            booking_end_time = data["booking_end_time"]
            booking_end_time = datetime.strptime(booking_end_time, '%H:%M:%S').time()
        else:
            booking_end_time = None

        today = datetime.today().date()

        if start_date != recurring_booking.start_date and start_date < today:
            return Response("Cant move start to the past.", status=status.HTTP_400_BAD_REQUEST)

        try:
            conflicts = recurring_booking.edit_recurring_booking(start_date,
                                                                 end_date,
                                                                 booking_start_time,
                                                                 booking_end_time,
                                                                 skip_conflicts,
                                                                 request.user)
            if conflicts is not None:
                return Response(conflicts, status=status.HTTP_409_CONFLICT)
            else:
                return Response(status=status.HTTP_200_OK)
        except (ValidationError, PrivilegeError) as error:
            if isinstance(error, PrivilegeError):
                return Response(error.message, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(error.message, status=status.HTTP_400_BAD_REQUEST)
