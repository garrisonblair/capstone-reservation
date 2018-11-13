from rest_framework.permissions import BasePermission
from apps.accounts.models.Booker import Booker


class IsBooker(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        try:
            booker = Booker.objects.get(user=request.user)
        except Booker.DoesNotExist:
            return False
        return True

    def has_object_permission(self, request, view, user):
        if request.user.is_superuser:
            return True

        try:
            booker = Booker.objects.get(user=request.user)
        except Booker.DoesNotExist:
            return False
        return True
