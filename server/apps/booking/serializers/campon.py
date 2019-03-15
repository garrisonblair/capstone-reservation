from rest_framework import serializers

from ..models.CampOn import CampOn
from ..models.Booking import Booking
from apps.accounts.models.User import User
from apps.accounts.serializers.user import UserSerializer
from apps.rooms.serializers.room import RoomSerializer


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


class LogCampOnSerializer(serializers.ModelSerializer):
    booker = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()

    class Meta:
        model = CampOn
        fields = ('id', 'booker', 'camped_on_booking', 'generated_booking', 'start_time', 'end_time', 'room')
        read_only_fields = ('id',)

    def get_booker(self, booking):
        return {"username": booking.booker.username, "id": booking.booker.id}

    def get_room(self, booking):
        return {"name": booking.room.name, "id": booking.room.id}


class MyCampOnSerializer(serializers.ModelSerializer):
    room = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    def get_room(self, obj):
        return RoomSerializer(obj.camped_on_booking.room).data

    def get_date(self, obj):
        return obj.camped_on_booking.date

    class Meta:
        model = CampOn
        fields = '__all__'
        read_only_fields = ('id',)
