from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.accounts.permissions.IsBooker import IsBooker
from rest_framework.generics import ListAPIView

from apps.booker_settings.serializers.personal_settings import PersonalSettingsSerializer


class PersonalSettingsCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = PersonalSettingsSerializer


class PersonalSettingsRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = PersonalSettingsSerializer
