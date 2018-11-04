from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ValidationError

from apps.accounts.serializers.privilege_category_serializer import PrivilegeCategorySerializer
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory


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
        request_name = request.query_params.get('name', None)

        if request_name is not None:
            categories = PrivilegeCategory.objects.filter(name=request_name)
            if categories.count() == 0:
                return Response("Category named {} does not exist".format(request_name),
                                status=status.HTTP_404_NOT_FOUND)
        else:
            categories = PrivilegeCategory.objects.all()

        category_list = list()
        for category in categories:
            serializer = PrivilegeCategorySerializer(category)
            category_list.append(serializer.data)
        return Response(category_list, status=status.HTTP_200_OK)
