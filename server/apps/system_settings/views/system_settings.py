from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions.IsOwnerOrAdmin import IsOwnerOrAdmin
from django.core.exceptions import ValidationError

from apps.accounts.permissions.IsSuperUser import IsSuperUser
from ..models.system_settings import SystemSettings
from ..serializers.system_settings import SystemSettingSerializer


class SystemSettingsAPI(APIView):

    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = SystemSettingSerializer

    def get(self, request):

        settings = SystemSettings.get_settings()

        serializer = SystemSettingSerializer(settings)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request):

        settings_updates = dict(request.data)

        settings = SystemSettings.get_settings()

        for key in settings_updates:
            setattr(settings, key, settings_updates[key])

        try:
            settings.save()
        except ValidationError as error:
            return Response(error.messages, status.HTTP_400_BAD_REQUEST)

        serializer = SystemSettingSerializer(settings)

        return Response(serializer.data, status.HTTP_200_OK)
