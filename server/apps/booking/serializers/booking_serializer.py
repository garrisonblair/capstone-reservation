from rest_framework import serializers
from ..models.Booking import Booking
from apps.accounts.serializers.UserSerializer import BookerSerializer


class BookingSerializer(serializers.ModelSerializer):

    booker = BookerSerializer()

    class Meta:
        model = Booking
        fields = ('id', 'booker', 'group', 'room', 'date', 'start_time', 'end_time')
        read_only_fields = ('id',)
