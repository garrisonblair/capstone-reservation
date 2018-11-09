from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes

from django.core.exceptions import ValidationError

from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.accounts.serializers.privilege_category_serializer import PrivilegeCategorySerializer
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory


@permission_classes((IsAuthenticated, IsSuperUser))
class PrivilegeCategoryView(APIView):
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

    def post(self, request):
        category_data = dict(request.data)
        serializer = PrivilegeCategorySerializer(data=category_data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = serializer.save()
            return Response(PrivilegeCategorySerializer(category).data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        category_data = dict(request.data)
        request_name = category_data.get("name")
        try:
            category = PrivilegeCategory.objects.get(name=request_name)
        except PrivilegeCategory.DoesNotExist:
            return Response("Category named {} does not exist".format(request_name),
                            status=status.HTTP_404_NOT_FOUND)
        serializer = PrivilegeCategorySerializer(instance=category, data=category_data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = serializer.save()
            return Response(PrivilegeCategorySerializer(category).data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)
