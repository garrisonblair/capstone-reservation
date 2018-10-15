from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ValidationError

from ..models.system_settings import SystemSettings
from ..serializers.system_settings_serializer import SystemSettingSerializer


class SystemSettingsAPI(APIView):

    def get(self, request):

        settings = SystemSettings.get_settings()

        serializer = SystemSettingSerializer(settings)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request):
        # TODO: add admin permission here when edwards branch is merged

        settings_updates = dict(request.data)

        settings = SystemSettings.get_settings()

        for key in settings_updates:
            setattr(settings, key, settings_updates[key][0])

        try:
            settings.save()
        except ValidationError as error:
            return Response(error.messages, status.HTTP_400_BAD_REQUEST)

        serializer = SystemSettingSerializer(settings)

        return Response(serializer.data, status.HTTP_200_OK)