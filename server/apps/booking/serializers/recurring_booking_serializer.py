from rest_framework import serializers

from ..models.Booking import RecurringBooking
from apps.rooms.models.Room import Room
from apps.groups.models.StudentGroup import StudentGroup
from apps.accounts.models.Student import Student


class RecurringBookingSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    booking_start_time = serializers.TimeField()
    booking_end_time = serializers.TimeField()
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    student_group = serializers.PrimaryKeyRelatedField(queryset=StudentGroup.objects.all())
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

    def create(self, validated_data):
        return RecurringBooking.objects.create_recurring_booking(
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
            start_time=validated_data["booking_start_time"],
            end_time=validated_data["booking_end_time"],
            room=validated_data["room"],
            student_group=validated_data["student_group"],
            student=validated_data["student"]
        )

    class Meta:
        model = RecurringBooking
        fields = '__all__'
