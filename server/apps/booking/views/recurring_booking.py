from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.booking.serializers.recurring_booking_serializer import RecurringBookingSerializer


class RecurringBookingView(APIView):
    def post(self, request):
        # Must be logged in as booker
        if not request.user or not request.user.booker:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        recurring_booking_data = dict(request.data)
        recurring_booking_data["booker"] = request.user.booker.booker_id

        serializer = RecurringBookingSerializer(data=recurring_booking_data)

        if not serializer.is_valid():
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                recurring_booking, conflicts = serializer.create(validated_data=serializer.validated_data)
                return Response(conflicts, status=status.HTTP_201_CREATED)
            except ValidationError as error:
                if error.message == "You must book as part of a verified group to create a recurring booking":
                    return Response(error.messages, status=status.HTTP_401_UNAUTHORIZED)
                elif ((error.message == "Start date can not be after End date.") or
                        (error.message == "You must book for at least two consecutive weeks.") or
                        (error.message == "Start time can not be after End time.")):
                    return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(error.messages, status=status.HTTP_409_CONFLICT)
