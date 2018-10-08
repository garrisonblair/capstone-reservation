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

        requestYear = request.GET.get('year')
        requestDay = request.GET.get('day')
        requestMonth = request.GET.get('month')

        print("requestYear: ")
        print(requestYear)
        print("requestMonth: ")
        print(requestMonth)
        print("requestDay: ")
        print(requestDay)

        if requestYear != None and requestMonth != None and requestDay != None:


            integerRequestYear = int(requestYear)
            integerRequestMonth = int(requestMonth)
            integerRequestDay = int(requestDay)

            date = datetime.date(integerRequestYear, integerRequestMonth, integerRequestDay)

            bookings = Booking.objects.filter(date=date)

        else:
            bookings = Booking.objects.all()

        bookingsList = list()
        for booking in bookings:
            serializer = BookingSerializer(booking)
            bookingsList.append(serializer.data)
        return Response(bookingsList, status=status.HTTP_200_OK)

