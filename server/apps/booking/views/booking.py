from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.models.Student import Student
from apps.booking.models.Booking import Booking

from apps.booking.serializers.booking_serializer import BookingSerializer

class BookingView(APIView):

    def post(self, request):


        print(request.data)

        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid():
            try:
                booking = serializer.save()
                return Response(BookingSerializer(booking).data)
            except ValidationError as error:
                return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)
