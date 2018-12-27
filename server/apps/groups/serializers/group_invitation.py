from rest_framework import serializers
from ..models.GroupInvitation import GroupInvitation
from ..serializers.group import ReadGroupSerializer
from apps.accounts.serializers.user import BookerSerializer


class ReadGroupInvitationSerializer(serializers.ModelSerializer):

    group = ReadGroupSerializer()
    invited_booker = BookerSerializer()

    class Meta:
        model = GroupInvitation
        fields = '__all__'


class WriteGroupInvitationSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupInvitation
        fields = '__all__'
        exclude = ['timestamp']
