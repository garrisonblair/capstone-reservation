from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions.IsBooker import IsBooker
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from apps.booker_settings.models.PersonalSettings import PersonalSettings
from apps.booker_settings.serializers.personal_settings import PersonalSettingsSerializer


class PersonalSettingsCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = PersonalSettingsSerializer


class PersonalSettingsUpdate(APIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = PersonalSettingsSerializer

    def patch(self, request, pk):
        try:
            personal_settings = PersonalSettings.objects.get(id=pk)
        except PersonalSettings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data

        # Booker id stays the same as its on creation
        if personal_settings.booker.id is request.user.id:
            data["booker"] = request.user.id
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = PersonalSettingsSerializer(personal_settings, data=data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            update_personal_settings = serializer.save()

            # Is not critical feature, does not need to be logged
            # utils.log_model_change(update_personal_settings, utils.CHANGE, request.user)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)


class PersonalSettingsList(ListAPIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = PersonalSettingsSerializer

    def get(self, request, pk):
        try:
            personal_settings = PersonalSettings.objects.get(id=pk)
        except PersonalSettings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if personal_settings.booker.id is not request.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(personal_settings, status=status.HTTP_200_OK)
