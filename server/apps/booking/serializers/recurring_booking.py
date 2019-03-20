from rest_framework import serializers

from apps.groups.serializers.group import ReadGroupSerializer
from ..models.RecurringBooking import RecurringBooking
from apps.rooms.models.Room import Room
from apps.groups.models.Group import Group
from apps.accounts.models.User import User
from apps.accounts.serializers.user import UserSerializer
from apps.rooms.serializers.room import RoomSerializer


class RecurringBookingSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    booking_start_time = serializers.TimeField()
    booking_end_time = serializers.TimeField()
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), allow_null=True)
    booker = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    skip_conflicts = serializers.BooleanField()

    def create(self, validated_data):
        return RecurringBooking.objects.create_recurring_booking(
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
            start_time=validated_data["booking_start_time"],
            end_time=validated_data["booking_end_time"],
            room=validated_data["room"],
            group=validated_data["group"],
            booker=validated_data["booker"],
            skip_conflicts=validated_data["skip_conflicts"]
        )

    class Meta:
        model = RecurringBooking
        fields = '__all__'


class ReadRecurringBookingSerializer(serializers.ModelSerializer):

    booker = UserSerializer(required=False)
    room = RoomSerializer(required=False)

    class Meta:
        model = RecurringBooking
        fields = ('id', 'start_date', 'end_date', 'booking_start_time', 'booking_end_time',
                  'room', 'group', 'booker', 'skip_conflicts')
        read_only_fields = ('id',)


class DetailedRecurringBookingSerializer(serializers.ModelSerializer):

    booker = UserSerializer(required=False)
    room = RoomSerializer(required=False)
    group = ReadGroupSerializer(required=False)

    class Meta:
        model = RecurringBooking
        fields = ('id', 'start_date', 'end_date', 'booking_start_time', 'booking_end_time',
                  'room', 'group', 'booker', 'skip_conflicts')
        read_only_fields = ('id',)


class PartialRecurringBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecurringBooking
        fields = ('id', 'start_date', 'end_date', 'booking_start_time', 'booking_end_time')
        read_only_fields = ('id',)


class LogRecurringBookingSerializer(serializers.ModelSerializer):
    booker = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()

    class Meta:
        model = RecurringBooking
        fields = ('id', 'start_date', 'end_date', 'booking_start_time', 'booking_end_time',
                  'room', 'group', 'booker', 'skip_conflicts')
        read_only_fields = ('id',)

    def get_booker(self, booking):
        return {"username": booking.booker.username, "id": booking.booker.id}

    def get_group(self, booking):
        if booking.group:
            return {"name": booking.group.name, "id": booking.group.id}

    def get_room(self, booking):
        return {"name": booking.room.name, "id": booking.room.id}
