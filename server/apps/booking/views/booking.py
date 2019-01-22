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
from apps.booking.models.Booking import BookingManager
from apps.booking.models.RecurringBooking import RecurringBooking
from apps.booking.models.CampOn import CampOn
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


class BookingCancel(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin, IsBooker)
    serializer_class = BookingSerializer

    def post(self, request, pk):
        # Ensure that booking to be canceled exists
        try:
            booking = Booking.objects.get(id=pk)
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check user permissions
        self.check_object_permissions(request, booking.booker)

        # Check if Booking has ended and if it has, disable booking from being canceled
        now = datetime.datetime.now()
        booking_end = booking.end_time
        timeout = now.time()

        if now.date() > booking.date or (now.date() == booking.date and timeout >= booking_end):
            return Response("Can't cancel booking anymore.", status=status.HTTP_403_FORBIDDEN)

        # Get all campons for this booking
        booking_id = booking.id
        booking_campons = list(CampOn.objects.filter(camped_on_booking__id=booking_id))

        # Remove any campons that have endtimes before current time
        for campon in booking_campons:
            if campon.end_time < timeout:
                booking_campons.remove(campon)

        # Checks to see if booking to cancel has any campons otherwise simply deletes the booking
        if len(booking_campons) <= 0:
            booking.delete()
        # Otherwise handles turning campons of original booking into campons for new booking and bookings if required
        else:
            # Sort list of campons by campon.id
            booking_campons.sort(key=booking_key, reverse=False)
            # Set first campon in list to first campon created
            first_campon = booking_campons[0]

            # Turn first campon (which should be first created) into a booking
            new_booking = Booking(booker=first_campon.booker,
                                  group=None,
                                  room=booking.room,
                                  date=now.date(),
                                  start_time=first_campon.start_time,
                                  end_time=first_campon.end_time)

            # Delete previous booking in order to then save new_booking derived from first campon,
            # then delete first campon
            booking.delete()
            new_booking.save()
            previous_campon = first_campon

            # Adding to see if I can iterate over all the rest without checking condition
            booking_campons.remove(first_campon)

            for campon in booking_campons:
                # Change associated booking of all other campons to booking id of new booking
                campon.camped_on_booking = new_booking
                # Creates booking for difference (Assuming current campon does not go into another booking)
                if (campon.end_time.hour > previous_campon.end_time.hour) \
                        or (campon.end_time.hour == previous_campon.end_time.hour and
                            (campon.end_time.minute - previous_campon.end_time.minute) > 10):
                    difference_booking = Booking(
                        booker=campon.booker,
                        group=None,
                        room=booking.room,
                        date=new_booking.date,
                        start_time=previous_campon.end_time,
                        end_time=campon.end_time)
                    difference_booking.save()
                    campon.end_time = difference_booking.start_time
                else:
                    campon.end_time = previous_campon.end_time
                campon.save()
                previous_campon = campon
            # Finally delete the first campon as it is now a new booking
            first_campon.delete()

        return Response(status=status.HTTP_200_OK)


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


class BookingViewMyBookings(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin, IsBooker)
    serializer_class = BookingSerializer

    def get_queryset(self, request):

        booker_id = request.user.id
        my_bookings = {}

        regular_bookings = Booking.objects.get(booker=booker_id)
        recurring_bookings = RecurringBooking.objects.get(booker=booker_id)
        campons = CampOn.objects.filter(booker=booker_id)

        my_bookings["regular_bookings"] = regular_bookings
        my_bookings["recurring_bookings"] = recurring_bookings
        my_bookings["campons"] = campons

        return my_bookings


def booking_key(val):
    return val.id

