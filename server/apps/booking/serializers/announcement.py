from rest_framework import serializers
from ..models.Announcement import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = ('id', 'title', 'content', 'begin_date', 'end_date')
        read_only_fields = ('id',)
