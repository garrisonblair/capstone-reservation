from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers.user import UserSerializerLogin


class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
            Login and returns user data with API token.
        """

        username = request.data.get('username')
        password = request.data.get('password')
        user = None

        user = authenticate(username=username, password=password)

        # Existing user in DB
        if user:
            login(request, user)
            serializer = UserSerializerLogin(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
