from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes

from django.core.exceptions import ValidationError

from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.accounts.serializers.privilege_category import PrivilegeCategorySerializer
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory


class PrivilegeCategoryList(ListAPIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = PrivilegeCategorySerializer
    queryset = PrivilegeCategory.objects.all()

    def get_queryset(self):
        qs = super(PrivilegeCategoryList, self).get_queryset()

        # Filter by name
        name = self.request.GET.get('name')
        if name:
            qs = PrivilegeCategory.objects.filter(name=name)

        return qs


class PrivilegeCategoryCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = PrivilegeCategorySerializer


class PrivilegeCategoryRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = PrivilegeCategorySerializer
    queryset = PrivilegeCategory.objects.all()
