from rest_framework import serializers

from ..models.Room import Room


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('id',
                  'name',
                  'capacity',
                  'number_of_computers',
                  'available',
                  'unavailable_start_time',
                  'unavailable_end_time',
                  'max_booking_duration',
                  'max_recurring_booking_duration')
        read_only_fields = ('id',)
