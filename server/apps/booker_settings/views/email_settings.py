from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.booker_settings.models.EmailSettings import EmailSettings as EmailSettingsModel
from apps.accounts.models.User import User
from apps.booker_settings.serializers.booker_settings import EmailSettingsSerializer
from django.core.exceptions import ValidationError

class EmailSettings(APIView):
    def patch(self, request):
        data = request.data

        email_settings = EmailSettingsModel.objects.get(booker=request.user)

        if "when_booking" in data:
            email_settings.when_booking = data["when_booking"]

        if "when_recurring_booking" in data:
            email_settings.when_recurring_booking = data["when_recurring_booking"]

        if "when_delete_booking" in data:
            email_settings.when_delete_booking = data["when_delete_booking"]

        if "when_delete_recurring_booking" in data:
            email_settings.when_delete_recurring_booking = data["when_delete_recurring_booking"]

        if "when_camp_on_booking" in data:
            email_settings.when_camp_on_booking = data["when_camp_on_booking"]

        try:
            email_settings.save()
        except ValidationError as error:
            return Response(error.message, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


    def get(self, request):
        email_settings = EmailSettingsModel.objects.get(booker=request.user)
        serializer = EmailSettingsSerializer(email_settings)

        return Response(serializer.data,status=status.HTTP_200_OK)
