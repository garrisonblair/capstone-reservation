from rest_framework import serializers

from ..models.Room import Room


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ('id',)
