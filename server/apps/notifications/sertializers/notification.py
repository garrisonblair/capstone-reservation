from rest_framework import serializers

from ..models.Notification import Notification


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('id',)
