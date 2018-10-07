from django.core.exceptions import ValidationError
from django.core import serializers
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.rooms.models.Room import Room
from apps.booking.models.Booking import Booking


class RoomView(APIView):
    def get(self, request, start_date_time='', end_date_time=''):
        if start_date_time != '' and end_date_time != '':
            start_date_time = datetime.strptime(start_date_time, "%Y-%m-%d %H:%M")
            end_date_time = datetime.strptime(end_date_time, "%Y-%m-%d %H:%M")

            if start_date_time < end_date_time:
                date = start_date_time.date()
                start_time = start_date_time.time()
                end_time = end_date_time.time()

                bookings = Booking.objects.filter(date=date, start_time__gte=start_time, end_time__lte=end_time)
                booked_rooms = []

                for booking in bookings:
                    booked_rooms.append(booking.room.pk)

                rooms = Room.objects.all().exclude(pk__in=booked_rooms)

                data = serializers.serialize("json", rooms)

                try:
                    return Response(data, status=status.HTTP_200_OK)
                except ValidationError as error:
                    return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        elif start_date_time == '' and end_date_time == '':
            data = serializers.serialize("json", Room.objects.all())

            try:
                return Response(data, status=status.HTTP_200_OK)
            except ValidationError as error:
                return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)
