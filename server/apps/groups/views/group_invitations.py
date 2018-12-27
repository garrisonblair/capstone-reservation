from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.permissions.IsBooker import IsBooker
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


class AcceptInvitation(APIView):

    permission_classes = (IsAuthenticated, IsBooker)

    def post(self, request, pk):

        try:
            invitation = GroupInvitation.objects.get(id=pk)
        except GroupInvitation.DoesNotExist:
            return Response("Invitation does not exist.", status.HTTP_412_PRECONDITION_FAILED)

        if request.user.booker.booker_id != invitation.invited_booker.booker_id:
            print('Here')
            print(request.user.booker.booker_id)
            print(invitation.invited_booker.booker_id)
            return Response("Can't accept this invitation", status.HTTP_401_UNAUTHORIZED)

        invitation.group.members.add(invitation.invited_booker.booker_id)

        return Response("Member added successfully.", status=status.HTTP_200_OK)
