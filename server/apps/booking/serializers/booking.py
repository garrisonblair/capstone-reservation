from rest_framework import serializers
from ..models.Booking import Booking, BookingSerializer
from apps.accounts.serializers.user import BookerSerializer


class ReadBookingSerializer(serializers.ModelSerializer):

    booker = BookerSerializer(required=False)

    class Meta:
        model = Booking
        fields = ('id', 'booker', 'group', 'room', 'date', 'start_time', 'end_time')
        read_only_fields = ('id',)
