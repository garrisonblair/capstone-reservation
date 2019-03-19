from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions.IsSuperUser import IsSuperUser

class CsvView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def get(self, request):
        return Response()
