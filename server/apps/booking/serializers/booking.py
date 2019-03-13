from rest_framework import serializers
from ..models.Booking import Booking
from apps.accounts.serializers.user import UserSerializer
from apps.groups.serializers.group import ReadGroupSerializer
from apps.rooms.serializers.room import RoomSerializer


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ('id',
                  'booker',
                  'group',
                  'room',
                  'date',
                  'start_time',
                  'end_time')
        read_only_fields = ('id',)


class AdminBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ('id',
                  'booker',
                  'group',
                  'room',
                  'date',
                  'start_time',
                  'end_time',
                  'bypass_privileges',
                  'bypass_validation',
                  'note',
                  'display_note',
                  'show_note_on_calendar')
        read_only_fields = ('id',)


class ReadBookingSerializer(serializers.ModelSerializer):

    booker = UserSerializer(required=False)
    group = ReadGroupSerializer(required=False)

    class Meta:
        model = Booking
        fields = ('id',
                  'booker',
                  'group',
                  'room',
                  'date',
                  'start_time',
                  'end_time',
                  'note',
                  'display_note',
                  'show_note_on_calendar',
                  'confirmed')
        read_only_fields = ('id',)


class DetailedBookingSerializer(serializers.ModelSerializer):

    booker = UserSerializer(required=False)
    group = ReadGroupSerializer(required=False)
    room = RoomSerializer(required=False)

    class Meta:
        model = Booking
        fields = ('id',
                  'booker',
                  'group',
                  'room',
                  'date',
                  'start_time',
                  'end_time',
                  'recurring_booking',
                  'note',
                  'display_note',
                  'confirmed')
        read_only_fields = ('id',)
