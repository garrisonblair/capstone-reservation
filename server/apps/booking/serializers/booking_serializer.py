from rest_framework import serializers
from ..models.Booking import Booking
from apps.accounts.serializers.UserSerializer import BookerSerializer


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ('id', 'booker', 'group', 'room', 'date', 'start_time', 'end_time')
        read_only_fields = ('id',)


class ReadBookingSerializer(serializers.ModelSerializer):

    booker = BookerSerializer(required=False)

    class Meta:
        model = Booking
        fields = ('id', 'booker', 'group', 'room', 'date', 'start_time', 'end_time')
        read_only_fields = ('id',)
