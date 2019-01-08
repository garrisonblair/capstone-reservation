from rest_framework import serializers

from ..models.CampOn import CampOn
from ..models.Booking import Booking
from apps.accounts.models.Booker import Booker
from apps.accounts.serializers.user import BookerSerializer


class CampOnSerializer(serializers.ModelSerializer):
    booker = serializers.PrimaryKeyRelatedField(queryset=Booker.objects.all())
    camped_on_booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())
    generated_booking = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CampOn
        fields = ('id', 'booker', 'camped_on_booking', 'generated_booking', 'start_time', 'end_time')
        read_only_fields = ('id',)


class ReadCampOnSerializer(serializers.ModelSerializer):
    booker = BookerSerializer(required=False)
    camped_on_booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())
    generated_booking = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CampOn
        fields = ('id', 'booker', 'camped_on_booking', 'generated_booking', 'start_time', 'end_time')
        read_only_fields = ('id',)
