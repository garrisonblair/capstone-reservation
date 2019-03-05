import datetime

from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.accounts.models.User import User
from apps.accounts.permissions.IsOwnerOrAdmin import IsOwnerOrAdmin
from apps.accounts.permissions.IsBooker import IsBooker
from apps.booking.models.Booking import Booking
from apps.booking.models.RecurringBooking import RecurringBooking
from apps.booking.models.CampOn import CampOn
from apps.booking.serializers.booking import \
    BookingSerializer, AdminBookingSerializer, ReadBookingSerializer, MyBookingSerializer
from apps.booking.serializers.recurring_booking import MyRecurringBookingSerializer
from apps.booking.serializers.campon import ReadCampOnSerializer
from apps.accounts.exceptions import PrivilegeError
from apps.notifications.models.Notification import Notification
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
        if request.user.is_superuser and "admin_selected_user" in data:
            data["booker"] = data["admin_selected_user"]
            del data["admin_selected_user"]
        else:
            data["booker"] = request.user.id

        if request.user.is_superuser:
            serializer = AdminBookingSerializer(data=data)
        else:
            serializer = BookingSerializer(data=data)

        now = datetime.datetime.now()

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        date = datetime.datetime.strptime(data["date"], '%Y-%m-%d').date()
        start_time = datetime.datetime.strptime(data["start_time"], '%H:%M:%S').time()

        if (date < now.date() or (date == now.date() and start_time < now.time())) and not request.user.is_superuser:
            return Response("Booking can not be made in the past", status=status.HTTP_401_UNAUTHORIZED)

        try:
            booking = serializer.save()
            booking.merge_with_neighbouring_bookings()
            booking.save()
            utils.log_model_change(booking, utils.ADDITION, request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ValidationError, PrivilegeError) as error:
            return Response(error.message, status=status.HTTP_400_BAD_REQUEST)


class BookingCancel(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin, IsBooker)
    serializer_class = BookingSerializer

    def post(self, request, pk):

        # Ensure that booking to be canceled exists
        try:
            booking = Booking.objects.get(id=pk)
        except Booking.DoesNotExist:
            return Response("Selected booking to cancel does not exist", status=status.HTTP_400_BAD_REQUEST)

        # Check user permissions
        self.check_object_permissions(request, booking.booker)

        # Check if Booking has ended and if it has, disable booking from being canceled
        now = datetime.datetime.now()
        booking_end = booking.end_time
        timeout = now.time()

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


class BookingRetrieveUpdateDestroy(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin, IsBooker)
    serializer_class = BookingSerializer

    def patch(self, request, pk):

        try:
            booking = Booking.objects.get(id=pk)
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if request.user.is_superuser and "admin_selected_user" in data:
            data["booker"] = data["admin_selected_user"]
            del data["admin_selected_user"]
        else:
            data["booker"] = request.user.id

        if not request.user.is_superuser:
            data["bypass_privileges"] = False

        # Check user permissions
        self.check_object_permissions(request, booking.booker)

        # Check if Booking started.
        now = datetime.datetime.now()

        settings = SystemSettings.get_settings()
        timeout = (now + settings.booking_edit_lock_timeout).time()

        # time = datetime.datetime.strptime(data["start_time"], "%H:%M").time()

        if "start_time" in data:
            if not datetime.datetime.strptime(data["start_time"], "%H:%M").time() == booking.start_time:
                if now.date() > booking.date or (now.date() == booking.date and timeout >= booking.start_time):
                    if not request.user.is_superuser:
                        return Response("Can't modify booking anymore.", status=status.HTTP_403_FORBIDDEN)

        data = request.data
        data["booker"] = booking.booker.id

        if "bypass_privileges" in data and not request.user.is_superuser:
            del data["bypass_privileges"]

        if request.user.is_superuser:
            serializer = AdminBookingSerializer(booking, data=data, partial=True)
        else:
            serializer = BookingSerializer(booking, data=data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            update_booking = serializer.save()

            utils.log_model_change(update_booking, utils.CHANGE, request.user)

            update_booking.merge_with_neighbouring_bookings()
            update_booking.save()

            utils.log_model_change(update_booking, utils.CHANGE, request.user)

            Notification.objects.notify(update_booking.date, update_booking.room)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)


class BookingViewMyBookings(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin, IsBooker)

    def get(self, request, pk):

        user = None
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check permissions
        self.check_object_permissions(request, user)

        bookings = dict()

        # Obtain all standard_bookings, recurring_bookings, and campons for this booker

        standard_bookings = user.get_active_non_recurring_bookings()
        recurring_bookings = RecurringBooking.objects.filter(booker=user)
        campons = CampOn.objects.filter(booker=user)

        # Insert standard_bookings and recurring_bookings made by groups that user is in
        for group in user.group_set.all():
            group_standard_bookings = group.get_active_non_recurring_bookings()
            standard_bookings = standard_bookings | group_standard_bookings

            group_recurring_bookings = RecurringBooking.objects.filter(~Q(booker=user), group=group)
            recurring_bookings = recurring_bookings | group_recurring_bookings

        # Add serialized lists of booking types to dictionary associated with type key
        bookings["standard_bookings"] = MyBookingSerializer(standard_bookings, many=True).data
        bookings["recurring_bookings"] = MyRecurringBookingSerializer(recurring_bookings, many=True).data
        bookings["campons"] = ReadCampOnSerializer(campons, many=True).data

        return Response(bookings, status=status.HTTP_200_OK)


class BookingConfirmation(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

    def post(self, request, pk):

        try:
            booking_to_confirm = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response("Booking does not exist", status=status.HTTP_400_BAD_REQUEST)

        self.check_object_permissions(request, booking_to_confirm.booker)

        today = datetime.datetime.now()
        time = today.time()
        if booking_to_confirm.date == today.date() and\
                booking_to_confirm.start_time <= time <= booking_to_confirm.end_time:
            booking_to_confirm.set_to_confirmed()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response("Can't confirm booking at this time", status=status.HTTP_400_BAD_REQUEST)


def booking_key(val):
    return val.id
