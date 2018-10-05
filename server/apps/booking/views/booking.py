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
