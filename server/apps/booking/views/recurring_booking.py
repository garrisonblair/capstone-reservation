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
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = RecurringBookingSerializer

    def post(self, request, pk):

        # Ensure that recurring booking to be canceled exists
        try:
            recurring_booking = RecurringBooking.objects.get(id=pk)
        except RecurringBooking.DoesNotExist:
            return Response('Booking does not exist.', status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_superuser:
            recurring_booking.delete()
            return Response("Recurring Booking deleted", status=status.HTTP_200_OK)

        # Check user permissions
        self.check_object_permissions(request, recurring_booking.booker)

        # Check if Booking has ended and if it has, disable booking from being canceled
        now = datetime.datetime.now()

        # Checks if current selected recurring booking has ended or not yet and handles accordingly
        if now.date() > recurring_booking.end_date \
                or (now.date() == recurring_booking.end_date):
            if not request.user.is_superuser:
                return Response("Selected booking cannot be canceled as booking has ended",
                                status=status.HTTP_400_BAD_REQUEST)

        # If it hasn't started yet delete entire recurring booking
        if now.date() < recurring_booking.start_date:
            recurring_booking.delete()
            return Response("Recurring Booking deleted", status=status.HTTP_200_OK)

        # Gets all future bookings associated to the indicated booking
        future_associated_booking_instances = recurring_booking.booking_set.filter(date__gt=now.date())
        future_associated_booking_instances.delete()

        try:
            recurring_booking.end_date = now.date() + datetime.timedelta(days=1)
            recurring_booking.save()
        except ValidationError as error:
            return Response(error.message, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
