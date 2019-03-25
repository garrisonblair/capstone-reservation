from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.booker_settings.models.EmailSettings import EmailSettings as EmailSettingsModel
from apps.booker_settings.serializers.booker_settings import EmailSettingsSerializer
from apps.util.Jwt import get_user_from_token
from django.core.exceptions import ValidationError


class EmailSettingsService(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        token = request.META['HTTP_AUTHORIZATION']
        user = get_user_from_token(token)
        try:
            email_settings = EmailSettingsModel.objects.get(booker=user)
            email_settings.update(data)
        except ValidationError as error:
            return Response(error.message, status=status.HTTP_400_BAD_REQUEST)
        except EmailSettingsModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        token = request.META['HTTP_AUTHORIZATION']
        user = get_user_from_token(token)
        email_settings = EmailSettingsModel.objects.get_or_create(booker=user)[0]
        serializer = EmailSettingsSerializer(email_settings)
        return Response(serializer.data, status=status.HTTP_200_OK)
