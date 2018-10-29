from rest_framework import serializers

from ..models.CampOn import CampOn
from ..models.Booking import Booking
from apps.accounts.models.Student import Student


class CampOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampOn
        fields = ('id', 'student', 'camped_on_booking', 'generated_booking', 'start_time', 'end_time')
        read_only_fields = ('id',)
