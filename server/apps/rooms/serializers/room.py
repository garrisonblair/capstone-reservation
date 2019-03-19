from rest_framework import serializers

from ..models.Room import Room


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('id', 'name', 'capacity', 'number_of_computers',
                  'available', 'unavailable_start_time', 'unavailable_end_time')
        read_only_fields = ('id',)
