from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ValidationError

from apps.accounts.models.User import User
from apps.booker_settings.models.EmailSettings import EmailSettings
from apps.accounts.permissions.IsBooker import IsBooker
from apps.groups.serializers.group import WriteGroupSerializer, ReadGroupSerializer
from apps.groups.models.Group import Group
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.system_administration.models.system_settings import SystemSettings

from ..models.GroupInvitation import GroupInvitation
from ..serializers.group_invitation import ReadGroupInvitationSerializer


class GroupList(ListAPIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = WriteGroupSerializer
    queryset = Group.objects.all()

    def get_queryset(self):
        qs = super(GroupList, self).get_queryset()
        try:
            if not self.request.user.is_superuser:
                user = User.objects.get(id=self.request.user.id)
                qs = user.group_set
        except User.DoesNotExist:
            pass

        return qs


class GroupCreate(APIView):
    permission_classes = (IsAuthenticated, IsBooker)

    def post(self, request):
        data = dict(request.data)

        try:
            owner = User.objects.get(id=request.user.id)
        except User.DoesNotExist as error:
            return Response(error.messages, status=status.HTTP_404_NOT_FOUND)

        data["owner"] = owner.id

        serializer = ReadGroupSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = serializer.save()
            group.members.add(owner)
            group.privilege_category = PrivilegeCategory.objects.get(is_default=True)
            group.save()

            serializer = WriteGroupSerializer(group)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)


class InviteMembers(APIView):
    permission_classes = (IsAuthenticated, IsBooker)

    def post(self, request, pk):
        group = Group.objects.get(id=pk)

        if group.owner.id != request.user.id:
            return Response("Cant modify this Group", status=status.HTTP_401_UNAUTHORIZED)

        settings = SystemSettings.get_settings()
        if settings.group_can_invite_after_privilege_set is False and not group.privilege_category.is_default:
            return Response("You can no longer invite members, now that you have approved group privileges",
                            status=status.HTTP_401_UNAUTHORIZED)

        members_to_invite = request.data["invited_bookers"]  # User.id list

        created_invitations = list()
        for user_id in members_to_invite:
            user = User.objects.get(id=user_id)

            try:
                existing_invitation = GroupInvitation.objects.get(invited_booker=user, group=group)
                existing_invitation.save()  # update timestamp
                created_invitations.append(existing_invitation)
                continue
            except GroupInvitation.DoesNotExist:
                invitation = GroupInvitation(invited_booker=user,
                                             group=group)
                invitation.save()
                created_invitations.append(invitation)

            email_settings = EmailSettings.objects.get_or_create(booker=user)[0]
            if email_settings.when_invitation:
                subject = "Capstone Room System: Group Invitation"
                message = "Hi {},\n" \
                          "You have been invited to the group {} by {}." \
                          "Please go to your profile to accept the invitation.".format(user.first_name,
                                                                                   group.name,
                                                                                   group.owner.username)
                user.send_email(subject, message)

        serializer = ReadGroupInvitationSerializer(created_invitations, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LeaveGroup(APIView):
    permission_classes = (IsAuthenticated, IsBooker)

    def post(self, request, pk):
        group = Group.objects.get(id=pk)
        leaving_member_id = request.user.id

        if group.owner.id != leaving_member_id:
            if group.members.filter(id=leaving_member_id).exists():
                group.members.remove(request.user.id)
                group.save()
        else:
            group.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


class RemoveMembers(APIView):
    permission_classes = (IsAuthenticated, IsBooker)

    def post(self, request, pk):
        group = Group.objects.get(id=pk)
        if group.owner.id != request.user.id:
            return Response("Can't modify this Group", status=status.HTTP_401_UNAUTHORIZED)
        members_to_remove = request.data["members"]

        for member_user_id in members_to_remove:
            booker_to_remove = User.objects.get(id=member_user_id)
            if booker_to_remove == group.owner:
                continue
            if group.members.filter(id=member_user_id).exists():
                group.members.remove(booker_to_remove)
        group.save()
        return Response(WriteGroupSerializer(group).data, status=status.HTTP_202_ACCEPTED)
