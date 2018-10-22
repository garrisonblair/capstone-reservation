from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.serializers.UserSerializer import UserSerializer


class MyUser(APIView):

    def get(self, request, format=None):
        if request.auth is not None:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        else:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)
