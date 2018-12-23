from rest_framework import serializers

from ..models.CampOn import CampOn
from ..models.Booking import Booking
from apps.accounts.models.Booker import Booker


class CampOnSerializer(serializers.ModelSerializer):
    booker = serializers.PrimaryKeyRelatedField(queryset=Booker.objects.all())
    camped_on_booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())
    generated_booking = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.SerializerMethodField()

    class Meta:
        model = CampOn
        fields = ('id', 'booker', 'camped_on_booking', 'generated_booking', 'start_time', 'end_time', 'username')
        read_only_fields = ('id',)

    def get_username(self, camp_on):
        return camp_on.booker.user.username
