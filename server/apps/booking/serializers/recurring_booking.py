from rest_framework import serializers

from ..models.Booking import RecurringBooking
from apps.rooms.models.Room import Room
from apps.groups.models.Group import Group
from apps.accounts.models.Booker import Booker


class RecurringBookingSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    booking_start_time = serializers.TimeField()
    booking_end_time = serializers.TimeField()
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), allow_null=True)
    booker = serializers.PrimaryKeyRelatedField(queryset=Booker.objects.all())
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
