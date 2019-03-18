from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.permissions.IsBooker import IsBooker
from rest_framework.permissions import IsAuthenticated

from apps.system_administration.models.system_settings import SystemSettings
from ..serializers.group_invitation import ReadGroupInvitationSerializer
from ..models.GroupInvitation import GroupInvitation


class GroupInvitationsList(ListAPIView):

    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = ReadGroupInvitationSerializer
    queryset = GroupInvitation.objects.all()

    def get_queryset(self):
        qs = super(GroupInvitationsList, self).get_queryset()

        if not self.request.user.is_superuser:
            qs = qs.filter(invited_booker=self.request.user.id)

        return qs


class AcceptInvitation(APIView):

    permission_classes = (IsAuthenticated, IsBooker)

    def post(self, request, pk):

        try:
            invitation = GroupInvitation.objects.get(id=pk)
        except GroupInvitation.DoesNotExist:
            return Response("Invitation does not exist.", status.HTTP_412_PRECONDITION_FAILED)

        if request.user.id != invitation.invited_booker.id:
            return Response("Can't accept this invitation", status.HTTP_401_UNAUTHORIZED)

        settings = SystemSettings.get_settings()
        if settings.group_can_invite_after_privilege_set is False \
                and not invitation.group.privilege_category.is_default:
            invitation.delete()
            return Response("You can no longer join this group, now that it has approved group privileges",
                            status=status.HTTP_401_UNAUTHORIZED)

        invitation.group.members.add(invitation.invited_booker)
        invitation.delete()

        return Response("Member added successfully.", status=status.HTTP_200_OK)


class RejectInvitation(APIView):

    permission_classes = (IsAuthenticated, IsBooker)

    def post(self, request, pk):

        try:
            invitation = GroupInvitation.objects.get(id=pk)
        except GroupInvitation.DoesNotExist:
            return Response("Invitation does not exist.", status.HTTP_412_PRECONDITION_FAILED)

        if request.user.id != invitation.invited_booker.id:
            return Response("Can't reject this invitation", status.HTTP_401_UNAUTHORIZED)

        invitation.delete()

        return Response("Invitation rejected.", status=status.HTTP_200_OK)


class RevokeInvitation(APIView):

    permission_classes = (IsAuthenticated, IsBooker)

    def post(self, request, pk):

        try:
            invitation = GroupInvitation.objects.get(id=pk)
        except GroupInvitation.DoesNotExist:
            return Response("Invitation does not exist.", status=status.HTTP_412_PRECONDITION_FAILED)

        if request.user.id != invitation.group.owner.id:
            return Response("Can't revoke this invitation", status.HTTP_401_UNAUTHORIZED)

        invitation.delete()

        return Response("Invitation revoked.", status.HTTP_200_OK)
