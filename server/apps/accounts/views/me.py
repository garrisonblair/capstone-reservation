from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import PrivilegeCategory
from apps.accounts.permissions.IsBooker import IsBooker
from apps.accounts.serializers.user import UserSerializer
from apps.accounts.models.User import User


class MyUser(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class MyPrivileges(APIView):
    permission_classes = (IsAuthenticated, IsBooker)

    def get(self, request):
        user = User.cast_django_user(request.user)
        privilege_merger = user.get_privileges()

        privileges = dict()
        my_privileges = dict()

        for field_name in PrivilegeCategory.get_parameter_names():
            if user.bookerprofile.privilege_categories.count() == 0:
                my_privileges[field_name] = ''
            else:
                my_privileges[field_name] = privilege_merger.get_parameter(field_name)

            privileges["me"] = my_privileges

        for group in user.group_set.all():

            privilege_merger = group.get_privileges()
            group_privileges = dict()

            for field_name in PrivilegeCategory.get_parameter_names():
                if group.privilege_category is None:
                    group_privileges[field_name] = ''
                else:
                    group_privileges[field_name] = privilege_merger.get_parameter(field_name)

            privileges[group.name] = group_privileges

        return Response(privileges, status=status.HTTP_200_OK)
