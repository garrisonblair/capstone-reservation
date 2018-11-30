from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes

from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.util.PrivilegeCategoryManager import PrivilegeCategoryManager


class PrivilegeCategoriesAssignSingle(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def patch(self, request, pk):

        try:
            booker = Booker.objects.get(pk=pk)
        except Booker.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Add Booker Privileges
        manager = PrivilegeCategoryManager()
        manager.assign_booker_privileges(booker)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PrivilegeCategoriesAssignAll(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def patch(self, request):

        try:
            # Add Privileges to all Bookers
            manager = PrivilegeCategoryManager()
            manager.assign_all_booker_privileges()
        except Booker.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)
