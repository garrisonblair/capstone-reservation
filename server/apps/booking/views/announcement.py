from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import ValidationError

from ..models.Announcement import Announcement
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.booking.serializers.announcement import AnnouncementSerializer
from apps.util import utils
from apps.accounts.exceptions import PrivilegeError


class AnnouncementList(ListAPIView):

    permission_classes = ()
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()

    def get_queryset(self):
        qs = super(AnnouncementList, self).get_queryset()

        # Filter by begin date
        begin_date = self.request.GET.get('begin_date')
        if begin_date:
            qs = qs.filter(begin_date=begin_date)

        # Filter by end date
        end_date = self.request.GET.get('end_date')
        if end_date:
            qs = qs.filter(end_date=end_date)

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

    def post(self, request, pk):

        try:
            announcement = Announcement.objects.get(id=pk)
        except announcement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check user permissions
        self.check_object_permissions(request, IsSuperUser)

        announcement.delete()
        utils.log_model_change(announcement, utils.CHANGE, request.user)

        return Response(status=status.Http_204)


class AnnouncementUpdate(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = AnnouncementSerializer

    def patch(self, request, pk):

        try:
            announcement = Announcement.objects.get(id=pk)
        except announcement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if request.user.is_superuser and "admin_selected_user" in data:
            data["booker"] = data["admin_selected_user"]
            del data["admin_selected_user"]
        else:
            data["booker"] = request.user.id

        if not request.user.is_superuser:
            data["bypass_privileges"] = False

        data = request.data

        serializer = AnnouncementSerializer(announcement, data=data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            update_announcement = serializer.save()

            utils.log_model_change(update_announcement, utils.CHANGE, request.user)
            update_announcement.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)
