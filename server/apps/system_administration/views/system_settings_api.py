from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions.IsOwnerOrAdmin import IsOwnerOrAdmin
from django.core.exceptions import ValidationError

from ..models.system_settings import SystemSettings
from ..serializers.system_settings_serializer import SystemSettingSerializer


class SystemSettingsAPI(APIView):

    def get(self, request):

        settings = SystemSettings.get_settings()

        serializer = SystemSettingSerializer(settings)

        return Response(serializer.data, status.HTTP_200_OK)

    @permission_classes((IsAuthenticated, IsOwnerOrAdmin))
    def patch(self, request):

        settings_updates = dict(request.data)

        settings = SystemSettings.get_settings()

        for key in settings_updates:
            print(key, settings_updates[key])
            setattr(settings, key, settings_updates[key])

        try:
            settings.save()
        except ValidationError as error:
            return Response(error.messages, status.HTTP_400_BAD_REQUEST)

        serializer = SystemSettingSerializer(settings)

        return Response(serializer.data, status.HTTP_200_OK)
