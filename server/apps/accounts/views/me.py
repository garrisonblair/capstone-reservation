from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.permissions.IsBooker import IsBooker
from apps.accounts.models.User import User
from apps.groups.models.Group import Group


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


class MyRecurringBookingPrivileges(APIView):
    permission_classes = (IsAuthenticated, IsBooker)

    def get(self, request):
        pk = self.request.query_params.get("pk")
        type = self.request.query_params.get("type")

        if type == "user":
            try:
                user = User.objects.get(id=pk)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        elif type == "group":
            try:
                user = Group.objects.get(id=pk)
            except Group.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        can_make_recurring_booking = user.get_privileges().get_parameter("can_make_recurring_booking")

        return Response(can_make_recurring_booking, status=status.HTTP_200_OK)
