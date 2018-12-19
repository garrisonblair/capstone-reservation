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
            booker = Booker.objects.get(pk=pk)
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
        booker_ids = data['bookers']
        category_id = data['privilege_category']

        try:
            privilege_category = PrivilegeCategory.objects.get(id=category_id)
        except PrivilegeCategory.DoesNotExist:
            return Response("Privilege category does not exist", status=status.HTTP_400_BAD_REQUEST)

        booker_qs = Booker.objects.all()

        for booker_id in booker_ids:
            try:
                booker = booker_qs.get(booker_id=booker_id)
                booker.privilege_categories.add(privilege_category)
            except Booker.DoesNotExist:
                print("Booker with id: {} does not exist.".format(booker_id))

        return Response(status=status.HTTP_200_OK)
