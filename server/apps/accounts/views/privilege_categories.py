from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ValidationError

from apps.accounts.serializers.privilege_category_serializer import PrivilegeCategorySerializer


class PrivilegeCategoryView(APIView):

    def post(self, request):
        # Must be logged in as admin
        # TODO: admin authentication

        category_data = dict(request.data)
        serializer = PrivilegeCategorySerializer(data=category_data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                category = serializer.save()
                return Response(PrivilegeCategorySerializer(category).data, status=status.HTTP_201_CREATED)
            except ValidationError as error:
                return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        pass
