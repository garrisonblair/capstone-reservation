from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


@permission_classes((IsAuthenticated, ))
class LogoutView(APIView):

    def get(self, request):
        """
            Remove API token
        """

        token = get_object_or_404(Token, user=request.user)
        token.delete()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
