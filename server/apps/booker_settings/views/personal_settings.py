from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.accounts.permissions.IsBooker import IsBooker
from rest_framework.generics import ListAPIView

from apps.booker_settings.serializers.booker_settings import EmailSettingsSerializer


class PersonalSettingsList(ListAPIView):
    permission_classes = (IsAuthenticated, IsBooker, IsSuperUser)
    serializer_class = EmailSettingsSerializer


class PersonalSettingsCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, IsBooker, IsSuperUser)
    serializer_class = EmailSettingsSerializer


class PersonalSettingsRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsBooker, IsSuperUser)
    serializer_class = EmailSettingsSerializer
    queryset = EmailSettingsSerializer.objects.all()
