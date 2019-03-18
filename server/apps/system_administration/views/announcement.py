from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import ValidationError

from apps.system_administration.models.Announcement import Announcement
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.system_administration.serializers.announcement import AnnouncementSerializer
from apps.util import utils
from apps.accounts.exceptions import PrivilegeError


class AnnouncementList(ListAPIView):

    permission_classes = ()
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()

    def get_queryset(self):
        qs = super(AnnouncementList, self).get_queryset()

        # Filter by begin date
        date = self.request.GET.get('date')
        try:
            if date:
                qs = qs.filter(start_date__lte=date, end_date__gte=date)
        except Exception:
            raise APIException

        return qs


class AnnouncementCreate(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = AnnouncementSerializer

    def post(self, request):
        data = request.data
        serializer = AnnouncementSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            announcement = serializer.save()
            utils.log_model_change(announcement, utils.ADDITION, request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except (ValidationError, PrivilegeError) as error:
            return Response(error.message, status=status.HTTP_400_BAD_REQUEST)


class AnnouncementDelete(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = AnnouncementSerializer

    def delete(self, request, pk):

        try:
            announcement = Announcement.objects.get(id=pk)
        except Announcement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        utils.log_model_change(announcement, utils.DELETION, request.user)
        announcement.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AnnouncementUpdate(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = AnnouncementSerializer

    def patch(self, request, pk):

        try:
            announcement = Announcement.objects.get(id=pk)
        except Announcement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data

        serializer = AnnouncementSerializer(announcement, data=data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            update_announcement = serializer.save()

            utils.log_model_change(update_announcement, utils.CHANGE, request.user)
            update_announcement.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        except (ValidationError, Exception) as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)
