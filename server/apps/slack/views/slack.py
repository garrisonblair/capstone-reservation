from datetime import datetime
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from rest_framework.response import Response
from rest_framework.views import APIView


class SlackView(APIView):

    def post(self, request):
        data = request.data

        print(data)

        return Response("Hello", status=status.HTTP_200_OK)
