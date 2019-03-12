from rest_framework import serializers
from ..models.EmailSettings import EmailSettings


class EmailSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailSettings
        fields = '__all__'
