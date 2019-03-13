from rest_framework import serializers

from apps.booking.serializers.booking import MyBookingSerializer
from ..models.CampOn import CampOn
from ..models.Booking import Booking
from apps.accounts.models.User import User
from apps.accounts.serializers.user import UserSerializer


class CampOnSerializer(serializers.ModelSerializer):
    booker = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    camped_on_booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())
    generated_booking = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CampOn
        fields = ('id', 'booker', 'camped_on_booking', 'generated_booking', 'start_time', 'end_time')
        read_only_fields = ('id',)


class ReadCampOnSerializer(serializers.ModelSerializer):
    booker = UserSerializer(required=False)
    camped_on_booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())
    generated_booking = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CampOn
        fields = ('id', 'booker', 'camped_on_booking', 'generated_booking', 'start_time', 'end_time')
        read_only_fields = ('id',)


class MyCampOnSerializer(serializers.ModelSerializer):
    camped_on_booking = MyBookingSerializer(required=False)

    class Meta:
        model = CampOn
        fields = '__all__'
        read_only_fields = ('id',)
