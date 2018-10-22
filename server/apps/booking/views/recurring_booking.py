from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.booking.serializers.recurring_booking_serializer import RecurringBookingSerializer


class RecurringBookingView(APIView):
    def post(self, request):
        # Must be logged in as student
        if not request.user or not request.user.student:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        recurring_booking_data = dict(request.data)
        recurring_booking_data["student"] = request.user.student.student_id

        serializer = RecurringBookingSerializer(data=recurring_booking_data)

        if not serializer.is_valid():
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                recurring_booking, conflicts = serializer.create(validated_data=serializer.validated_data)
                return Response(conflicts, status=status.HTTP_201_CREATED)
            except ValidationError as error:
                return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)
