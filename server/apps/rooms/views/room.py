from datetime import datetime
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.booking.models.Booking import Booking
from apps.rooms.models.Room import Room
from apps.rooms.serializers.room import RoomSerializer


# TODO: Refactor
class RoomList(APIView):
    permission_classes = ()
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    def get(self, request):
        start_date_time = request.GET.get('start_date_time')
        end_date_time = request.GET.get('end_date_time')
        qs = Room.objects.all()

        # Query returns all rooms when no time slot is provided
        if not start_date_time and not end_date_time:
            serializer = RoomSerializer(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Time interval parameters provided
        elif start_date_time and end_date_time:
            try:
                start_date_time = datetime.strptime(start_date_time, "%Y-%m-%d %H:%M")
                end_date_time = datetime.strptime(end_date_time, "%Y-%m-%d %H:%M")

                # Time format is valid
                if start_date_time < end_date_time:
                    date = start_date_time.date()
                    start_time = start_date_time.time()
                    end_time = end_date_time.time()

                    bookings = Booking.objects.filter(date=date, start_time__gte=start_time, end_time__lte=end_time)
                    booked_rooms = list()
                    for booking in bookings:
                        booked_rooms.append(booking.room.pk)

                    qs = qs.exclude(pk__in=booked_rooms)  # Booked rooms excluded from the query
                    serializer = RoomSerializer(qs, many=True)

                    try:
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    except ValidationError as error:
                        return Response(error, status=status.HTTP_400_BAD_REQUEST)
                else:
                    error_msg = "Invalid times: start time must be before end time"
                    return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)  # Invalid time format
            except (ValueError, TypeError):
                error_msg = "Invalid parameters, please input parameters in the YYYY-MM-DD HH:mm format"
                return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        # When only one of start time and end time is provided
        else:
            error_msg = "Invalid times: please supply a start time and an end time"
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)


class RoomCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = RoomSerializer


class RoomRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
