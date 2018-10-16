from rest_framework import serializers

from ..models.CampOn import CampOn

class CampOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampOn
        fields = ('id', 'student', 'booking', 'start_time', 'end_time')
        read_only_fields = ('id',)
