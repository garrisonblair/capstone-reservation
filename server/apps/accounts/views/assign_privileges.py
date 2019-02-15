from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models.User import User
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory

from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.util.PrivilegeCategoryManager import PrivilegeCategoryManager


class PrivilegeCategoriesAssignSingleAutomatic(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def patch(self, request, pk):

        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Add Booker Privileges
        manager = PrivilegeCategoryManager()
        manager.assign_booker_privileges(user)

        return Response(status=status.HTTP_200_OK)


class PrivilegeCategoriesAssignAllAutomatic(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def patch(self, request):

        manager = PrivilegeCategoryManager()
        manager.assign_all_booker_privileges()

        return Response(status=status.HTTP_200_OK)


class PrivilegeCategoriesAssignManual(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def patch(self, request):

        data = request.data
        user_ids = data['users']
        category_id = data['privilege_category']

        try:
            privilege_category = PrivilegeCategory.objects.get(id=category_id)
        except PrivilegeCategory.DoesNotExist:
            return Response("Privilege category does not exist", status=status.HTTP_400_BAD_REQUEST)

        user_qs = User.objects.all()
        ids_do_not_exist = list()

        for user_id in user_ids:
            try:
                user = user_qs.get(id=user_id)
                user.bookerprofile.privilege_categories.add(privilege_category)
            except User.DoesNotExist:
                ids_do_not_exist.append(user_id)

        return Response(ids_do_not_exist, status=status.HTTP_200_OK)


class PrivilegeCategoriesRemoveManual(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def patch(self, request):

        data = request.data
        user_ids = data['users']
        category_id = data['privilege_category']

        try:
            privilege_category = PrivilegeCategory.objects.get(id=category_id)
            if privilege_category.is_default:
                return Response("Default privilege category cannot be deleted",
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                default_category = PrivilegeCategory.objects.get(is_default=True)
        except PrivilegeCategory.DoesNotExist:
            return Response("Privilege category does not exist", status=status.HTTP_400_BAD_REQUEST)

        user_qs = User.objects.all()
        ids_do_not_exist = list()

        for user_id in user_ids:
            try:
                user = user_qs.get(id=user_id)
                user.bookerprofile.privilege_categories.remove(privilege_category)
                if len(user.bookerprofile.privilege_categories.all()) is 0:
                    user.bookerprofile.privilege_categories.add(default_category)
            except User.DoesNotExist:
                ids_do_not_exist.append(user_id)

        return Response(ids_do_not_exist, status=status.HTTP_200_OK)
