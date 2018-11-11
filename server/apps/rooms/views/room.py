from django.core.exceptions import ValidationError
from datetime import datetime

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from apps.booking.models.Booking import Booking
from apps.rooms.models.Room import Room
from apps.rooms.serializers.room_serializer import RoomSerializer


class RoomView(APIView):
    def get(self, request):
        start_date_time = request.query_params.get('start_date_time', '')
        end_date_time = request.query_params.get('end_date_time', '')

        # Query returns all rooms when no time slot is provided
        if start_date_time == '' and end_date_time == '':
            rooms = Room.objects.all()
            room_list = list()
            for room in rooms:
                serializer = RoomSerializer(room)
                room_list.append(serializer.data)

            try:
                return Response(room_list, status=status.HTTP_200_OK)
            except ValidationError as error:
                return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)

        # Time interval parameters provided
        elif start_date_time != '' and end_date_time != '':
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

                    rooms = Room.objects.all().exclude(pk__in=booked_rooms)  # Booked rooms excluded from the query

                    room_list = list()
                    for room in rooms:
                        serializer = RoomSerializer(room)
                        room_list.append(serializer.data)

                    try:
                        return Response(room_list, status=status.HTTP_200_OK)
                    except ValidationError as error:
                        return Response(error, status=status.HTTP_400_BAD_REQUEST)

                else:
                    error_msg = "Invalid times: start time must be before end time"
                    return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)  # Invalid time format
            except (ValueError, TypeError):
                error_msg = "Invalid parameters, please input parameters in the YYYY-MM-DD HH:mm format"
                return Response(error_msg,
                                status=status.HTTP_400_BAD_REQUEST)

        # When only one of start time and end time is provided
        else:
            error_msg = "Invalid times: please supply a start time and an end time"
            return Response(error_msg,
                            status=status.HTTP_400_BAD_REQUEST)


class RoomCreateView(APIView):

    @permission_classes((IsAuthenticated, IsSuperUser))
    def post(self, request, *args, **kwargs):

        if not request.user or request.user.is_superuser is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        room_data = dict(request.data)

        serializer = RoomSerializer(data=room_data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                room = serializer.save()
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
            except ValidationError as error:
                return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)


class RoomUpdateView(APIView):

    @permission_classes((IsAuthenticated, IsSuperUser))
    def patch(self, request, *args, **kwargs):

        if not request.user or request.user.is_superuser is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        room_data = dict(request.data)
        room_id = room_data['room_id']
        capacity = room_data['capacity']
        number_of_computers = room_data['number_of_computers']

        room = None

        try:
            room = Room.objects.get(room_id=room_id)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if room_id:
            room.room_id = room_id

        if capacity:
            room.capacity = capacity

        if number_of_computers:
            room.number_of_computers = number_of_computers

        serializer = RoomSerializer(room, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                room = serializer.save()
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            except ValidationError as error:
                return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)


class RoomDeleteView(APIView):

    @permission_classes((IsAuthenticated, IsSuperUser))
    def delete(self, request, *args, **kwargs):

        if not request.user or request.user.is_superuser is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        room_id = request.data.get('room_id')

        room = None

        try:
            room = Room.objects.get(room_id=room_id)
        except Room.DoesNotExist:
            return Response("Invalid room. Please provide an existing room", status=status.HTTP_404_NOT_FOUND)

        try:
            room.delete()
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(status=status.HTTP_400_BAD_REQUEST)
