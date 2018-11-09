from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers.UserSerializer import UserSerializer


class MyUser(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
