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
from apps.booking.serializers.recurring_booking import RecurringBookingSerializer
from apps.util import utils


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
        except RecurringBooking.DoesNotExist:
            return Response("Selected recurring booking to cancel does not exist", status=status.HTTP_400_BAD_REQUEST)

        # Check user permissions
        self.check_object_permissions(request, booking.booker)

        delete_all_instances = request.data['delete_all_instances']

        # Check if Booking has ended and if it has, disable booking from being canceled
        now = datetime.datetime.now()
        booking_end = booking.end_time
        timeout = now.time()

        if not delete_all_instances:

            if now.date() > booking.date or (now.date() == booking.date and timeout >= booking_end):
                if not request.user.is_superuser:
                    return Response("Selected booking cannot be canceled as booking has started",
                                    status=status.HTTP_400_BAD_REQUEST)

            try:
                booking.delete_booking()
                utils.log_model_change(booking, utils.DELETION, request.user)
            except ValidationError as e:
                return Response(e.message, status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_200_OK)

        else:
            # Gets the parent recurring booking
            associated_recurring_booking = booking.recurring_booking

            # Checks if current selected recurring booking has started or not yet and handles accordingly
            if now.date() > booking.date or (now.date() == booking.date and timeout >= booking_end):
                if not request.user.is_superuser:
                    return Response("Selected booking cannot be canceled as booking has started",
                                    status=status.HTTP_400_BAD_REQUEST)

            try:
                # Deletes the indicated booking
                booking.delete_booking()
                utils.log_model_change(booking, utils.DELETION, request.user)

                # Gets all bookings associated to the indicated booking
                all_associated_booking_instances = Booking.objects.get(recurring_booking=associated_recurring_booking)

                for associated_booking in all_associated_booking_instances:

                    # If the date of the recurring booking is after the current indicated booking date, try to delete
                    if associated_booking.date > now.date():
                            associated_booking.delete_booking()
                            utils.log_model_change(booking, utils.DELETION, request.user)

            except ValidationError as e:
                return Response(e.message, status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_200_OK)





