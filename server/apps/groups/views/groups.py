from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings
from django.core import mail
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

from apps.accounts.permissions.IsBooker import IsBooker
from apps.accounts.models.Booker import Booker
from apps.groups.serializers.group import WriteGroupSerializer, ReadGroupSerializer
from apps.groups.models.Group import Group
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory

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
                booker = self.request.user.booker
                qs = booker.groups
        except Booker.DoesNotExist:
            pass

        return qs


class GroupCreate(APIView):
    permission_classes = (IsAuthenticated, IsBooker)

    def post(self, request):
        data = dict(request.data)

        try:
            owner = Booker.objects.get(booker_id=request.user.booker.booker_id)
        except Group.DoesNotExist as error:
            return Response(error.messages, status=status.HTTP_404_NOT_FOUND)

        data["owner"] = owner.booker_id

        serializer = ReadGroupSerializer(data=data)

        if not serializer.is_valid():
            print("invalid")
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


class AddMembers(APIView):
    permission_classes = (IsAuthenticated, IsBooker)

    def post(self, request, pk):
        group = Group.objects.get(id=pk)
        if group.owner != request.user.booker:
            return Response("Can't modify this Group", status=status.HTTP_401_UNAUTHORIZED)
        members_to_add = request.data["members"]
        for member_id in members_to_add:
            if not group.members.filter(booker_id=member_id).exists():
                group.members.add(member_id)
            else:
                print("Booker {} is already in group".format(member_id))
        group.save()
        return Response(WriteGroupSerializer(group).data, status=status.HTTP_202_ACCEPTED)


class InviteMembers(APIView):
    permission_classes = (IsAuthenticated, IsBooker)

    def post(self, request, pk):
        group = Group.objects.get(id=pk)

        if group.owner != request.user.booker:
            return Response("Cant modify this Group", status=status.HTTP_401_UNAUTHORIZED)

        members_to_invite = request.data["invited_bookers"]  # User.id list

        created_invitations = list()
        for user_id in members_to_invite:
            user = User.objects.get(id=user_id)

            try:
                existing_invitation = GroupInvitation.objects.get(invited_booker=user.booker, group=group)
                existing_invitation.save()  # update timestamp
                created_invitations.append(existing_invitation)
                continue
            except GroupInvitation.DoesNotExist:
                invitation = GroupInvitation(invited_booker=user.booker,
                                             group=group)
                invitation.save()
                created_invitations.append(invitation)

            subject = "Capstone Room System: Group Invitation"
            message = "Hi {},\n"\
                      "You have been invited to the group {} by {}."\
                      "Press on the link below to accept the invitation.".format(user.first_name,
                                                                                 group.name,
                                                                                 group.owner.user.username)

            mail.send_mail(subject,
                           message,
                           settings.EMAIL_HOST_USER,
                           [user.email])

        serializer = ReadGroupInvitationSerializer(created_invitations, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RemoveMembers(APIView):
    permission_classes = (IsAuthenticated, IsBooker)

    def post(self, request, pk):
        group = Group.objects.get(id=pk)
        if group.owner != request.user.booker:
            return Response("Can't modify this Group", status=status.HTTP_401_UNAUTHORIZED)
        members_to_remove = request.data["members"]
        for member_id in members_to_remove:
            if member_id == group.owner.booker_id:
                print("Owner can not be removed from group")
                continue
            if group.members.filter(booker_id=member_id).exists():
                group.members.remove(member_id)
            else:
                print("Booker {} is not in the group".format(member_id))
        group.save()
        return Response(WriteGroupSerializer(group).data, status=status.HTTP_202_ACCEPTED)
