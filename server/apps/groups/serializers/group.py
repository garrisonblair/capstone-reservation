from rest_framework import serializers
from ..models.Group import Group
from ..models.PrivilegeRequest import PrivilegeRequest

from apps.accounts.serializers.user import UserSerializer


class WriteGroupSerializer(serializers.ModelSerializer):

    owner = UserSerializer()
    members = UserSerializer(many=True)
    group_invitations = serializers.SerializerMethodField()
    privilege_request = serializers.SerializerMethodField()

    def get_group_invitations(self, group):
        from apps.groups.serializers.group_invitation import GroupContextInvitationSerializer
        return GroupContextInvitationSerializer(group.invitations, many=True).data

    def get_privilege_request(self, group):
        from apps.groups.serializers.privilege_request import ReadPrivilegeRequestSerializer
        try:
            group.privilegerequest
        except PrivilegeRequest.DoesNotExist:
            return
        return ReadPrivilegeRequestSerializer(group.privilegerequest).data

    class Meta:
        model = Group
        fields = '__all__'


class ReadGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'
