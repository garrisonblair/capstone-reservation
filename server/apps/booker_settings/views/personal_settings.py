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


class PersonalSettingsCreateRetrieveUpdate(APIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = PersonalSettingsSerializer

    def post(self, request):
        data = request.data

        try:
            email_settings = PersonalSettings.objects.get(booker=request.user)
        except PersonalSettings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            # Booker id stays the same as its on creation
            data["booker"] = request.user.id
            email_settings.update(data)
        except ValidationError as error:
            return Response(error.message, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        personal_settings = PersonalSettings.objects.get_or_create(booker=request.user)[0]
        serializer = PersonalSettingsSerializer(personal_settings)

        return Response(serializer.data, status=status.HTTP_200_OK)
