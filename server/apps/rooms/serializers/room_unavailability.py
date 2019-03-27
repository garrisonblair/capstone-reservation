from rest_framework import serializers

from ..models.RoomUnavailability import RoomUnavailability


class RoomUnavailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomUnavailability
        fields = ('id', 'room', 'start_time', 'end_time')
        read_only_fields = ('id',)
