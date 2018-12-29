from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ValidationError

from apps.accounts.permissions.IsBooker import IsBooker
from apps.accounts.models.Booker import Booker
from apps.groups.serializers.group import WriteGroupSerializer, ReadGroupSerializer
from apps.groups.models.Group import Group
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory


class GroupList(ListAPIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = WriteGroupSerializer
    queryset = Group.objects.all()

    def get_queryset(self):
        qs = super(GroupList, self).get_queryset()
        try:
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
            owner = Booker.objects.get(id=request.user.booker.id)
        except Group.DoesNotExist as error:
            return Response(error.messages, status=status.HTTP_404_NOT_FOUND)

        data["owner"] = owner.id

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
            if not group.members.filter(id=member_id).exists():
                group.members.add(member_id)
            else:
                print("Booker {} is already in group".format(member_id))
        group.save()
        return Response(WriteGroupSerializer(group).data, status=status.HTTP_202_ACCEPTED)


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
            if group.members.filter(id=member_id).exists():
                group.members.remove(member_id)
            else:
                print("Booker {} is not in the group".format(member_id))
        group.save()
        return Response(WriteGroupSerializer(group).data, status=status.HTTP_202_ACCEPTED)
