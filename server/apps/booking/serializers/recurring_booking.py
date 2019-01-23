from rest_framework import serializers

from ..models.RecurringBooking import RecurringBooking
from apps.rooms.models.Room import Room
from apps.groups.models.Group import Group
from apps.accounts.models.User import User
from apps.accounts.serializers.user import UserSerializer


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

    class Meta:
        model = RecurringBooking
        fields = ('id', 'start_date', 'end_date', 'booking_start_time', 'booking_end_time',
                  'room', 'group', 'booker', 'skip_conflicts')
        read_only_fields = ('id',)
