from rest_framework import serializers
from ..models.PersonalSettings import PersonalSettings


class PersonalSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalSettings
        fields = '__all__'
