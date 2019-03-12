from rest_framework import serializers

from apps.rooms.serializers.room import RoomSerializer
from ..models.Notification import Notification


class WriteNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('id',)


class ReadNotificationSerializer(serializers.ModelSerializer):

    rooms = RoomSerializer(many=True)

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('id',)
