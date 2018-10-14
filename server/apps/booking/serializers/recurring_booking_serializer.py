from rest_framework import serializers

from ..models.Booking import RecurringBooking


class RecurringBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringBooking
        fields = ('id', 'start_date', 'end_date', 'booking_start_time', 'booking_end_time',
                  'room', 'student_group', 'student')
        read_only_fields = ('id',)
