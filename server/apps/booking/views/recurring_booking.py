from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.permissions.IsBooker import IsBooker
from apps.accounts.exceptions import PrivilegeError
from apps.booking.serializers.recurring_booking import RecurringBookingSerializer


class RecurringBookingCreate(APIView):
    permission_classes = (IsAuthenticated, IsBooker)

    def post(self, request):

        recurring_booking_data = dict(request.data)
        recurring_booking_data["booker"] = request.user.booker.booker_id

        serializer = RecurringBookingSerializer(data=recurring_booking_data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                recurring_booking, conflicts = serializer.create(validated_data=serializer.validated_data)
                return Response(conflicts, status=status.HTTP_201_CREATED)
            except (ValidationError, PrivilegeError) as error:
                if isinstance(error, PrivilegeError):
                    return Response(error.message, status=status.HTTP_401_UNAUTHORIZED)
                elif ((error.message == "Start date can not be after End date.") or
                        (error.message == "You must book for at least two consecutive weeks.") or
                        (error.message == "Start time can not be after End time.")):
                    return Response(error.message, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(error.message, status=status.HTTP_409_CONFLICT)
