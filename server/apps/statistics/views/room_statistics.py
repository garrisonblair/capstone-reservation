import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.rooms.models import Room
from apps.statistics.util.RoomStatisticManager import RoomStatisticManager


class RoomStatistics(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def get(self, request):
        room_ids = request.GET.getlist('room')
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')

        if start_date is not None:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        if end_date is not None:
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        manager = RoomStatisticManager()
        rooms_stats = list()

        if len(room_ids) == 0:
            rooms = Room.objects.all()
            for room in rooms:
                rooms_stats.append(manager.get_serialized_statistics(room, start_date, end_date))

        else:
            for room_id in room_ids:
                try:
                    room = Room.objects.get(id=room_id)
                    rooms_stats.append(manager.get_serialized_statistics(room, start_date, end_date))
                except Room.DoesNotExist:
                    print("Room with ID: {} does not exist".format(room_id))

        if len(rooms_stats) == 0:
            return Response("Rooms by these IDs do not exist", status.HTTP_400_BAD_REQUEST)

        return Response(rooms_stats, status.HTTP_200_OK)
