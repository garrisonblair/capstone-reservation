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


class LogBookingSerializer(serializers.ModelSerializer):

    booker = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ('id',
                  'booker',
                  'group',
                  'room',
                  'date',
                  'start_time',
                  'end_time',
                  'recurring_booking',)
        read_only_fields = ('id',)

    def get_booker(self, booking):
        return {"username": booking.booker.username, "id": booking.booker.id}

    def get_group(self, booking):
        if booking.group:
            return {"name": booking.group.name, "id": booking.group.id}

    def get_room(self, booking):
        return {"name": booking.room.name, "id": booking.room.id}
