from rest_framework import serializers

from ..models.Room import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('room_id', 'capacity', 'number_of_computers')
