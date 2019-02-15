from rest_framework import serializers
from apps.system_administration.models.Announcement import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = ('id', 'title', 'content', 'start_date', 'end_date')
        read_only_fields = ('id',)
