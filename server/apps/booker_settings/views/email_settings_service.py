from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.booker_settings.models.EmailSettings import EmailSettings as EmailSettingsModel
from apps.accounts.models.User import User
from apps.booker_settings.serializers.booker_settings import EmailSettingsSerializer
from apps.util.Jwt import getUserFromToken
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed

class EmailSettingsService(APIView):
    authentication_classes = ()
    permission_classes = ()
    def post(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        token = request.META['HTTP_AUTHORIZATION']
        user = getUserFromToken(token)
        email_settings = EmailSettingsModel.objects.get(booker=user)
        try:
            email_settings.update(data)
        except ValidationError as error:
            return Response(error.message, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


    def get(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        token = request.META['HTTP_AUTHORIZATION']
        user = getUserFromToken(token)
        email_settings = EmailSettingsModel.objects.get_or_create(booker=user)[0]
        serializer = EmailSettingsSerializer(email_settings)
        return Response(serializer.data,status=status.HTTP_200_OK)
