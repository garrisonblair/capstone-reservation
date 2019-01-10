from rest_framework import serializers
from ..models.Group import Group

from apps.accounts.serializers.user import BookerSerializer


class WriteGroupSerializer(serializers.ModelSerializer):

    owner = BookerSerializer()
    members = BookerSerializer(many=True)
    group_invitations = serializers.SerializerMethodField()

    def get_group_invitations(self, group):
        from apps.groups.serializers.group_invitation import GroupContextInvitationSerializer
        return GroupContextInvitationSerializer(group.invitations, many=True).data

    class Meta:
        model = Group
        fields = '__all__'


class ReadGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'
