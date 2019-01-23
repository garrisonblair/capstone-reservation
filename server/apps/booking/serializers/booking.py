from rest_framework import serializers
from ..models.Booking import Booking
from apps.accounts.serializers.user import UserSerializer
from apps.groups.serializers.group import ReadGroupSerializer
from apps.rooms.serializers.room import RoomSerializer


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ('id', 'booker', 'group', 'room', 'date', 'start_time', 'end_time', 'bypass_privileges')
        read_only_fields = ('id',)


class ReadBookingSerializer(serializers.ModelSerializer):

    booker = UserSerializer(required=False)

    class Meta:
        model = Booking
        fields = ('id', 'booker', 'group', 'room', 'date', 'start_time', 'end_time')
        read_only_fields = ('id',)


class MyBookingSerializer(serializers.ModelSerializer):

    booker = UserSerializer(required=False)
    group = ReadGroupSerializer(required=False)
    room = RoomSerializer(required=False)

    class Meta:
        model = Booking
        fields = ('id', 'booker', 'group', 'room', 'date', 'start_time', 'end_time', 'recurring_booking')
        read_only_fields = ('id',)
