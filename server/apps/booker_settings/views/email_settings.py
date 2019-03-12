from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.booker_settings.models.EmailSettings import EmailSettings as EmailSettingsModel
from apps.accounts.models.User import User
from apps.booker_settings.serializers.booker_settings import EmailSettingsSerializer

class EmailSettings(APIView):
    def patch(self, request):
        data = request.data
        when_booking = "when_booking"
        if not when_booking in data:
            return Response("'{}' is missing in request body".format(when_booking), status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


    def get(self, request):
        email_settings = EmailSettingsModel.objects.get(booker=request.user)
        serializer = EmailSettingsSerializer(email_settings)
        return Response(serializer.data,status=status.HTTP_200_OK)
