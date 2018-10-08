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

    def get(self, request, *args, **kwargs):

        print("request: ")
        print(request)

        print("*args: ")
        print(*args)

        print("**kwargs: ")
        print(**kwargs)

        print("request.data: ")
        booking_data = dict(request.data)
        print(booking_data)
        defaultYear = datetime.date.year
        print(defaultYear)
        defaultMonth = datetime.date.month
        print(defaultMonth)
        defaultDay = datetime.date.day
        print(defaultDay)

        #requestYear = request.GET.get('year', defaultYear)
        #requestMonth = request.GET.get('month', defaultMonth)
        #requestDay = request.GET.get('day', defaultDay)

        requestYear = request.GET.get('year')
        print("requestYear: ")
        print(requestYear)
        requestMonth = request.GET.get('month')
        print("requestMonth: ")
        print(requestMonth)
        requestDay = request.GET.get('day')
        print("requestDay: ")
        print(requestDay)
        requestDate = request.GET.get('date')
        print("requestDate: ")
        print(requestDate)

        # Need to modify hardcoded values below once front-end finalizes format
        integerRequestYear = 2018
        integerRequestMonth = 10
        integerRequestDay = 6

        #integerRequestYear = int(requestYear)
        #integerRequestMonth = int(requestMonth)
        #integerRequestDay = int(requestDay)

        date = datetime.date(integerRequestYear, integerRequestMonth, integerRequestDay)
        #date = datetime.date(requestYear, requestMonth, requestDay)

        bookings = Booking.objects.filter(date=date)

        bookingsList = list()
        for booking in bookings:
            serializer = BookingSerializer(booking)
            bookingsList.append(serializer.data)
        return Response(bookingsList, status=status.HTTP_200_OK)

