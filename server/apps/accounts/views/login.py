from django.contrib.auth import authenticate, login, get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.ldap_server import get_ldap_connection
from apps.accounts.serializers.UserSerializer import UserSerializerLogin


# TODO: Send email
class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
            Get user data and API token
        """

        username = request.data.get('username')
        password = request.data.get('password')
        user = None

        # Non-verified user
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass

        if user:
            if not user.is_active:
                print("Non-verified user")
                return Response(status=status.HTTP_302_FOUND)
        else:
            # New user from LDAP
            connection = get_ldap_connection()
            user = connection.get_user(username=username)

            if user:
                print("New LDAP user")
                user.is_active = False
                user.save()
                # Send email
                return Response(status=status.HTTP_201_CREATED)

        user = authenticate(username=username, password=password)

        # Existing user in DB
        if user:
            print("Existing user")
            login(request, user)
            serializer = UserSerializerLogin(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
