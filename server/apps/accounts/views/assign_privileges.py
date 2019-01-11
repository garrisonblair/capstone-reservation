from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models.Booker import Booker
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory

from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.util.PrivilegeCategoryManager import PrivilegeCategoryManager


class PrivilegeCategoriesAssignSingleAutomatic(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def patch(self, request, pk):

        try:
            booker = Booker.objects.get(id=pk)
        except Booker.DoesNotExist:
            print("No Booker is here")
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Add Booker Privileges
        manager = PrivilegeCategoryManager()
        manager.assign_booker_privileges(booker)

        return Response(status=status.HTTP_200_OK)


class PrivilegeCategoriesAssignAllAutomatic(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def patch(self, request):

        try:
            # Add Privileges to all Bookers
            manager = PrivilegeCategoryManager()
            manager.assign_all_booker_privileges()
        except Booker.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

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

        ids_do_not_exist = list()

        for user_id in user_ids:
            try:
                booker = Booker.objects.get(user__username=user_id)
                booker.privilege_categories.add(privilege_category)
            except Booker.DoesNotExist:
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
        except PrivilegeCategory.DoesNotExist:
            return Response("Privilege category does not exist", status=status.HTTP_400_BAD_REQUEST)

        ids_do_not_exist = list()

        for user_id in user_ids:
            try:
                booker = Booker.objects.get(user__username=user_id)
                booker.privilege_categories.remove(privilege_category)
            except Booker.DoesNotExist:
                ids_do_not_exist.append(user_id)

        return Response(ids_do_not_exist, status=status.HTTP_200_OK)
