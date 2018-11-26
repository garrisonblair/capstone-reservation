from django.contrib.auth import login
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models.VerificationToken import VerificationToken
from apps.accounts.serializers.user import UserSerializerLogin


# TODO: Verify expiration time
class VerifyView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
            Verify a user with a given token.
        """

        token = request.data.get('token')
        verification_token = None
        try:
            verification_token = VerificationToken.objects.get(token=token)
        except VerificationToken.DoesNotExist:
            pass

        if verification_token:
            user = verification_token.user
            user.is_active = True
            user.save()
            login(request, user)
            serializer = UserSerializerLogin(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
