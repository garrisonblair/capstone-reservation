from rest_framework import serializers
from ..models.Booking import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'student', 'student_group', 'room', 'date', 'start_time', 'end_time')
        read_only_fields = ('id',)
