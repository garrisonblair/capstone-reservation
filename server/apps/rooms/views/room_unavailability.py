from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import APIException

from apps.rooms.models.RoomUnavailability import RoomUnavailability
from apps.rooms.serializers.room_unavailability import RoomUnavailabilitySerializer


class RoomUnavailabilityList(ListAPIView):
    permission_classes = ()
    serializer_class = RoomUnavailabilitySerializer
    queryset = RoomUnavailability.objects.all()

    def get_queryset(self):
        qs = super(RoomUnavailabilityList, self).get_queryset()

        try:
            room_id = self.request.GET.get('room_id')
            date_time = self.request.GET.get('date_time')

            # Filter by room
            if room_id:
                qs = qs.filter(room__id=room_id)

            # Filter by dateTime
            if date_time:
                qs = qs.filter(start_time__lte=date_time, end_time__gte=date_time)

        except Exception:
            raise APIException

        return qs


class RoomUnavailabilityCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = RoomUnavailabilitySerializer


class RoomUnavailabilityRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = RoomUnavailabilitySerializer
    queryset = RoomUnavailability.objects.all()
