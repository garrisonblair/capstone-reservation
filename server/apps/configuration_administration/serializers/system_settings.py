from rest_framework.serializers import ModelSerializer

from ..models.system_settings import SystemSettings


class SystemSettingSerializer(ModelSerializer):
    class Meta:
        model = SystemSettings
        exclude = ("webcalendar_username",
                   "webcalendar_password")
