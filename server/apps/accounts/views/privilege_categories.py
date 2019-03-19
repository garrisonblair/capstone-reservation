from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from apps.accounts.permissions.IsBooker import IsBooker
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.accounts.serializers.privilege_category import PrivilegeCategorySerializer, ReadPrivilegeCategorySerializer
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory


class PrivilegeCategoryList(ListAPIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = ReadPrivilegeCategorySerializer
    queryset = PrivilegeCategory.objects.all()

    def get_queryset(self):
        qs = super(PrivilegeCategoryList, self).get_queryset()

        try:
            # Filter by name
            name = self.request.GET.get('name')
            if name:
                qs = PrivilegeCategory.objects.filter(name=name)
        except Exception:
            raise APIException

        return qs


class MyPrivilegeCategoryList(ListAPIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = ReadPrivilegeCategorySerializer

    def get_queryset(self):
        booker = self.request.user.bookerprofile
        qs = booker.privilege_categories

        return qs


class PrivilegeCategoryCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = PrivilegeCategorySerializer


class PrivilegeCategoryRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = PrivilegeCategorySerializer
    queryset = PrivilegeCategory.objects.all()
