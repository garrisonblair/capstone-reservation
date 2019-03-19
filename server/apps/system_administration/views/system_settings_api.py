from datetime import timedelta
import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions.IsOwnerOrAdmin import IsOwnerOrAdmin
from django.core.exceptions import ValidationError

from ..models.system_settings import SystemSettings
from ..serializers.system_settings_serializer import SystemSettingSerializer


class ReadSystemSettings(APIView):
    permission_classes = ()

    def get(self, request):

        settings = SystemSettings.get_settings()
        serializer = SystemSettingSerializer(settings)

        return Response(serializer.data, status.HTTP_200_OK)


class SystemSettingsAPI(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

    def patch(self, request):

        settings_updates = dict(request.data)

        settings = SystemSettings.get_settings()

        for key in settings_updates:
            if key == "booking_edit_lock_timeout" or key == "default_time_to_notify_before_booking":
                duration_str = settings_updates[key]
                duration_split = duration_str.split(" ")
                if len(duration_split) == 2:
                    duration_time = duration_split[1]
                    duration_day = int(duration_split[0])
                else:
                    duration_time = duration_split[0]
                    duration_day = 0

                time = datetime.datetime.strptime(duration_time, "%H:%M:%S")
                settings_updates[key] = timedelta(days=duration_day,
                                                  hours=time.hour,
                                                  minutes=time.minute,
                                                  seconds=time.second)

            setattr(settings, key, settings_updates[key])

        try:
            settings.save()
        except ValidationError as error:
            return Response(error.messages, status.HTTP_400_BAD_REQUEST)

        serializer = SystemSettingSerializer(settings)

        return Response(serializer.data, status.HTTP_200_OK)
