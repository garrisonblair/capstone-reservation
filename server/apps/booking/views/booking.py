import datetime

from django.core.exceptions import ValidationError


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.booking.models.Booking import Booking

from apps.booking.serializers.booking_serializer import BookingSerializer


class BookingView(APIView):

    def post(self, request):

        # Must be logged in as booker
        if not request.user or request.user.booker is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        booking_data = dict(request.data)
        booking_data["booker"] = request.user.booker.booker_id

        serializer = BookingSerializer(data=booking_data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                booking = serializer.save()
                return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
            except ValidationError as error:
                return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        request_year = request.GET.get('year')
        request_day = request.GET.get('day')
        request_month = request.GET.get('month')

        if request_year is not None and request_month is not None and request_day is not None:

            try:

                integer_request_year = int(request_year)
                integer_request_month = int(request_month)
                integer_request_day = int(request_day)

                date = datetime.date(integer_request_year, integer_request_month, integer_request_day)
                bookings = Booking.objects.filter(date=date)

            except ValueError:
                return Response("Invalid date. Please supply valid integer values for year, month and day",
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                bookings = Booking.objects.all()
            except ValidationError as error:
                return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)

        bookings_list = list()
        for booking in bookings:
            serializer = BookingSerializer(booking)
            bookings_list.append(serializer.data)
        return Response(bookings_list, status=status.HTTP_200_OK)

    def patch(self, request, booking_id):
        # Must be logged in as booker
        if not request.user or request.user.booker is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        booking = self.get_booking(booking_id)
        serializer = BookingSerializer(booking, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                update_booking = serializer.save()
                return Response(BookingSerializer(update_booking).data, status=status.HTTP_204_NO_CONTENT)
            except ValidationError as error:
                return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)

    def get_booking(self, booking_id):
        return Booking.objects.get(id=booking_id)
