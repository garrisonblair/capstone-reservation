import datetime

from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.models.Student import Student
from apps.booking.models.Booking import Booking

from apps.booking.serializers.booking_serializer import BookingSerializer


class BookingView(APIView):

    def post(self, request):

        # Must be logged in as student
        if not request.user or not request.user.student:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        booking_data = dict(request.data)
        booking_data["student"] = request.user.student.student_id

        serializer = BookingSerializer(data=booking_data)

        if not serializer.is_valid():
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                booking = serializer.save()
                return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
            except ValidationError as error:
                return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        defaultYear = datetime.date.year
        print(defaultYear)
        defaultMonth = datetime.date.month
        print(defaultMonth)
        defaultDay = datetime.date.day
        print(defaultDay)

        requestYear = request.GET.get('year', defaultYear)
        requestMonth = request.GET.get('month', defaultMonth)
        requestDay = request.GET.get('day', defaultDay)

        # Need tl modify hardcoded values below once front-end finalizes format
        integerRequestYear = 2018
        integerRequestMonth = 10
        integerRequestDay = 6

        date = datetime.date(integerRequestYear, integerRequestMonth, integerRequestDay)
        print(date)
        bookings = Booking.objects.filter(date=date)
        print(bookings)
        bookingsList = list()
        for booking in bookings:
            serializer = BookingSerializer(booking)
            bookingsList.append(serializer.data)
        return Response(bookingsList, status=status.HTTP_200_OK)

