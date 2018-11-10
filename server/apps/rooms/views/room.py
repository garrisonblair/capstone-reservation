from django.core.exceptions import ValidationError
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.rooms.models.Room import Room
from apps.booking.models.Booking import Booking
from apps.rooms.serializers.room_serializer import RoomSerializer

# Added by Steve
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions.IsOwnerOrAdmin import IsAdmin


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

    @permission_classes((IsAuthenticated, IsAdmin))
    def post(self, request, *args, **kwargs):

        room_data = dict(request.data)

        room = None

        capacity = room_data['capacity']

        if not isinstance(capacity, int):
            return Response("Invalid capacity. Please enter a positive integer value or zero",
                            status=status.HTTP_400_BAD_REQUEST)

        number_of_computers = room_data['number_of_computers']

        if not isinstance(number_of_computers, int):
            return Response("Invalid number of computers. Please enter a positive integer value or zero",
                            status=status.HTTP_400_BAD_REQUEST)

        if capacity < 0:
            return Response("Invalid capacity. Please enter a positive integer value or zero",
                            status=status.HTTP_400_BAD_REQUEST)

        if (capacity % 1) != 0:
            return Response("Invalid capacity. Please enter a positive integer value or zero",
                            status=status.HTTP_400_BAD_REQUEST)

        if int(number_of_computers) < 0:
            return Response("Invalid number of computers. Please enter a positive integer value or zero",
                            status=status.HTTP_400_BAD_REQUEST)

        if (number_of_computers % 1) != 0:
            return Response("Invalid Number of computers. Please enter a positive integer value or zero",
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Room.objects.get(room_id=room_data['room_id'])
        except Room.DoesNotExist:
            if room_data['room_id'] is not '':
                new_room = Room(room_id=room_data['room_id'],
                                capacity=capacity,
                                number_of_computers=number_of_computers)
                new_room.save()
                return Response("Room does not exist. Creating room",
                                status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        room_id = room_data.get('room_id')
        room = Room.objects.get(room_id=room_id)
        room.capacity = capacity
        room.number_of_computers = number_of_computers

        try:
            room.save()
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes((IsAuthenticated, IsAdmin))
    def delete(self, request, *args, **kwargs):

        room_data = dict(request.data)

        room = None

        try:
            room = Room.objects.get(room_id=room_data["room_id"])
        except Room.DoesNotExist:
            return Response("Invalid room. Please provide an existing room",
                            status=status.HTTP_404_NOT_FOUND)

        try:
            room.delete()
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.message, status=status.HTTP_400_BAD_REQUEST)
