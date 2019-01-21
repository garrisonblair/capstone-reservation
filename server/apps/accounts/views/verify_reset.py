from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models.VerificationToken import VerificationToken
from apps.accounts.serializers.user import UserSerializerLogin


# TODO: Verify expiration time
class VerifyResetView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
            Verify a user with a given token.
        """

        token = request.data.get('token')
        password = request.data.get('password')

        try:
            verification_token = VerificationToken.objects.get(token=token)
        except VerificationToken.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if verification_token:
            user = verification_token.user
            user.password = make_password(password)
            user.save()
            serializer = UserSerializerLogin(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
