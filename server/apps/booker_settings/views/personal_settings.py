from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.accounts.permissions.IsBooker import IsBooker
from rest_framework.generics import ListAPIView

from apps.rooms.models.RoomUnavailability import RoomUnavailability
from apps.rooms.serializers.room_unavailability import RoomUnavailabilitySerializer


class PersonalSettingsList(ListAPIView):
    permission_classes = (IsAuthenticated, IsBooker, IsSuperUser)
    serializer_class = RoomUnavailabilitySerializer


class PersonalSettingsCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, IsBooker, IsSuperUser)
    serializer_class = RoomUnavailabilitySerializer


class PersonalSettingsRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsBooker, IsSuperUser)
    serializer_class = RoomUnavailabilitySerializer
    queryset = RoomUnavailability.objects.all()
