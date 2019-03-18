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

        # Ensure that recurring booking to be canceled exists
        try:
            booking = Booking.objects.get(id=pk)
        except Booking.DoesNotExist as e:
            return Response('Booking does not exist.', status=status.HTTP_400_BAD_REQUEST)

        # Check user permissions
        self.check_object_permissions(request, booking.booker)

        # Check if Booking has ended and if it has, disable booking from being canceled
        now = datetime.datetime.now()
        booking_end = booking.end_time
        timeout = now.time()

        # Gets the parent recurring booking
        associated_recurring_booking = booking.recurring_booking

        # Checks if current selected recurring booking has started or not yet and handles accordingly
        if now.date() > booking.date or (now.date() == booking.date and timeout >= booking_end):
            if not request.user.is_superuser:
                return Response("Selected booking cannot be canceled as booking has started",
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            # Gets all bookings associated to the indicated booking
            all_associated_booking_instances = associated_recurring_booking.booking_set.all()

            for associated_booking in all_associated_booking_instances:

                # If the date of the recurring booking is after the current indicated booking date, try to delete
                if associated_booking.date >= now.date():
                    associated_booking.delete_booking()
                    utils.log_model_change(booking, utils.DELETION, request.user)

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

        # Ensure that recurring booking to be modifed exists
        try:
            booking = Booking.objects.get(id=pk)
        except Booking.DoesNotExist:
            return Response("Selected booking to edit does not exist", status=status.HTTP_400_BAD_REQUEST)

        # Check user permissions
        self.check_object_permissions(request, booking.booker)

        now = datetime.datetime.now()
        booking_end = booking.end_time
        timeout = now.time()
        data = request.data
        skip_conflicts = request.data['skip_conflicts']

        # Gets the parent recurring booking
        associated_recurring_booking = booking.recurring_booking

        # Checks if current selected recurring booking has started or not yet and handles accordingly
        if now.date() > booking.date or (now.date() == booking.date and timeout >= booking_end):
            if not request.user.is_superuser:
                return Response("Selected booking cannot be modified as booking has started",
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            all_conflicts = []
            non_conflicting_bookings = []

            # Gets all bookings associated to the indicated booking
            all_associated_booking_instances = associated_recurring_booking.booking_set.all()

            # FInd the earliest booking in the list
            earliest_booking = all_associated_booking_instances[0]
            for booking in all_associated_booking_instances:
                if booking.start_date < earliest_booking.start_date:
                    earliest_booking = booking

            # Determine offset based on earlist booking
            booking_offset = earliest_booking - data["start_date"]

            # Get current end date and apply offset in case start date has changed
            end_date = data["end_date"]
            current_end_date = associated_recurring_booking.end_date
            current_end_date = current_end_date + datetime.timedelta(days=booking_offset)

            # Create new bookings if new end date has been extended and add to appropriate lists
            while current_end_date < end_date:
                # Sets the next booking in series
                current_end_date = current_end_date + datetime.timedelta(days=7)
                if current_end_date < end_date:
                    try:
                        booking = Booking.objects.create_booking(
                            booker=associated_recurring_booking.booker,
                            group=associated_recurring_booking.group,
                            room=associated_recurring_booking.room,
                            date=current_end_date,
                            start_time=data["booking_start_time"],
                            end_time=data["booking_end_time"],
                            recurring_booking=associated_recurring_booking,
                            confirmed=False
                        )
                        non_conflicting_bookings.add(booking)
                    except ValidationError:
                        if not skip_conflicts:
                            all_conflicts.append(booking)
                        else:
                            continue

            # Iterates through associated bookings and makes the adjustment
            for associated_booking in all_associated_booking_instances:

                # Modify the start and end times as needed
                if "booking_start_time" in data:
                    associated_booking.start_time = data["booking_start_time"]
                if "booking_end_time" in data:
                    associated_booking.end_time = data["booking_end_time"]

                recurring_booking, conflicts = RecurringBooking.objects.edit_recurring_booking(
                    start_date=associated_booking.start_date + datetime.timedelta(days=booking_offset),
                    end_date=associated_booking.end_date + datetime.timedelta(days=booking_offset),
                    start_time=associated_booking.booking_start_time,
                    end_time=associated_booking.booking_end_time,
                    room=associated_booking.room,
                    group=associated_booking.group,
                    booker=associated_booking.booker,
                    skip_conflicts=associated_booking.skip_conflicts
                )

                if len(conflicts) != 0 and not skip_conflicts:
                    for conflict in conflicts:
                        all_conflicts.append(conflict)
                else:
                    non_conflicting_bookings.append(associated_booking)

            # If there are no conflicts, simply make adjustments accordingly
            if len(all_conflicts) == 0 or skip_conflicts:
                for non_conflicting in non_conflicting_bookings:
                    # Make sure bookings are in range and have not ended before modifying
                    if non_conflicting.end_date <= data["end_date"] and \
                            non_conflicting.start_date >= data["start_date"] and \
                            non_conflicting.start_date >= now.date():
                        non_conflicting.save()
                        utils.log_model_change(booking, utils.CHANGE, request.user)
                    # Make sure bookings are in range and have not ended before deleting. Can't delete past bookings
                    elif non_conflicting.start_date >= data["start_date"] and \
                            non_conflicting.start_date >= now.date():
                        non_conflicting.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                # If there are any conflicts, return list of them
                return Response(all_conflicts, status=status.HTTP_409_CONFLICT)

        except (ValidationError, PrivilegeError) as error:
            if isinstance(error, PrivilegeError):
                return Response(error.message, status=status.HTTP_401_UNAUTHORIZED)
            elif ((error.message == "You must book for at least two consecutive weeks.") or
                  (error.message == "Start time can not be after End time.")):
                return Response(error.message, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(error.message, status=status.HTTP_409_CONFLICT)

        return Response(status=status.HTTP_200_OK)
