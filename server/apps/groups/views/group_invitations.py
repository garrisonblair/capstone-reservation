from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from apps.accounts.permissions import IsBooker
from rest_framework.permissions import IsAuthenticated

from ..serializers.group_invitation import ReadGroupInvitationSerializer
from ..models.GroupInvitation import GroupInvitation

from apps.accounts.models.Booker import Booker


class GroupInvitationsList(ListAPIView):

    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = ReadGroupInvitationSerializer
    queryset = GroupInvitation.objects.all()

    def get_queryset(self):
        qs = super(GroupInvitationsList, self).get_queryset()

        if not self.request.user.is_superuser:
            try:
                invited_booker = Booker.objects.get(booker_id=self.request.user.booker)
                qs.filter(invited_booker=invited_booker)
            except Booker.DoesNotExist:
                pass

        return qs
