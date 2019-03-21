from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.booker_settings.models.EmailSettings import EmailSettings as EmailSettingsModel
from apps.accounts.models.User import User
from apps.booker_settings.serializers.booker_settings import EmailSettingsSerializer
from django.core.exceptions import ValidationError

class EmailSettings(APIView):
    def post(self, request):
        data = request.data

        email_settings = EmailSettingsModel.objects.get(booker=request.user)

        try:
            email_settings.update(data)
        except ValidationError as error:
            return Response(error.message, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


    def get(self, request):
        email_settings = EmailSettingsModel.objects.get_or_create(booker=request.user)[0]
        serializer = EmailSettingsSerializer(email_settings)

        return Response(serializer.data,status=status.HTTP_200_OK)
