from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.permissions.IsBooker import IsBooker
from apps.accounts.models.Booker import Booker
from apps.groups.serializers.group import GroupSerializer
from apps.groups.models.Group import Group


class GroupList(ListAPIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def get_queryset(self):
        qs = super(GroupList, self).get_queryset()
        try:
            booker = self.request.user.booker
            qs = booker.group_set.all()
        except Booker.DoesNotExist:
            pass

        return qs
