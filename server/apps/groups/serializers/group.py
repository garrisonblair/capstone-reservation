from rest_framework import serializers
from ..models.Group import Group

from apps.accounts.serializers.user import BookerSerializer


class WriteGroupSerializer(serializers.ModelSerializer):

    owner = BookerSerializer()
    members = BookerSerializer(many=True)

    class Meta:
        model = Group
        fields = '__all__'


class ReadGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'
