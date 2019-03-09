from datetime import datetime
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.rooms.models.Room import Room
from apps.rooms.serializers.room import RoomSerializer


class RoomList(APIView):
    permission_classes = ()
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    def get(self, request):
        date = request.GET.get('date')
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        qs = Room.objects.all()

        if date and start_time and end_time:
            try:
                date = datetime.strptime(date, "%Y-%m-%d").date()
                start_time = datetime.strptime(start_time, "%H:%M").time()
                end_time = datetime.strptime(end_time, "%H:%M").time()
            except (ValueError, TypeError) as error:
                print(error)
                error_msg = "Invalid parameters, please input parameters in the YYYY-MM-DD HH:mm format"
                return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

            for room in qs:
                if not room.is_available(date, start_time, end_time):
                    qs.exclude(room)

            if qs.count() == 0:
                return Response("No available rooms", status=status.HTTP_404_NOT_FOUND)

        serializer = RoomSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = RoomSerializer


class RoomRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
