from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.booker_settings.models.PersonalSettings import PersonalSettings
from apps.booker_settings.serializers.personal_settings import PersonalSettingsSerializer
from apps.util.Jwt import get_user_from_token
from django.core.exceptions import ValidationError


class PersonalSettingsService(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        token = request.META['HTTP_AUTHORIZATION']
        user = get_user_from_token(token)
        try:
            personal_settings = PersonalSettings.objects.get(booker=user)
            personal_settings.update(data)
        except ValidationError as error:
            return Response(error.message, status=status.HTTP_400_BAD_REQUEST)
        except PersonalSettings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        token = request.META['HTTP_AUTHORIZATION']
        user = get_user_from_token(token)
        personal_settings = PersonalSettings.objects.get_or_create(booker=user)[0]
        serializer = PersonalSettingsSerializer(personal_settings)
        return Response(serializer.data, status=status.HTTP_200_OK)
