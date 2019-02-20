from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.accounts.models.User import User
from apps.accounts.permissions.IsBooker import IsBooker
from apps.notifications.models.Notification import Notification
from apps.notifications.sertializers.notification import NotificationSerializer


class NotificationList(ListAPIView):
    permission_classes = (IsBooker, IsAuthenticated)
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get_queryset(self):
        qs = super(NotificationList, self).get_queryset()

        if not self.request.user.is_superuser:
            try:
                user = User.objects.get(id=self.request.user.id)
                qs = user.notification_set
            except User.DoesNotExist as error:
                return Response(error.messages, status=status.HTTP_404_NOT_FOUND)

        # Filter by day
        date = self.request.GET.get('date')
        if date:
            qs = qs.filter(date=date)

        return qs


class NotificationCreate(APIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = NotificationSerializer

    def post(self, request):
        data = request.data

        try:
            user = User.objects.get(id=request.user.id)
            data["booker"] = user.id
        except User.DoesNotExist as error:
            return Response(error.messages, status=status.HTTP_404_NOT_FOUND)

        serializer = NotificationSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            notification = serializer.save()
        except ValidationError as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)

        result = notification.check_all_room_availability()
        if not result:
            return Response("Notification request was successfully created", status=status.HTTP_201_CREATED)

        available_room = dict()
        available_room["room"] = result[0].id
        available_room["start_time"] = result[1].time
        available_room["end_time"] = result[2].times

        return Response(available_room, status=status.HTTP_200_OK)
