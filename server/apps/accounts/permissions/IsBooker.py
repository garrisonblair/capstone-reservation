from rest_framework.permissions import BasePermission
from apps.accounts.models.Booker import Booker


class IsBooker(BasePermission):
    def has_permission(self, request, view):
        # Admin can overwrite permission
        if request.user.is_superuser:
            return True

        try:
            booker = Booker.objects.get(user=request.user)
        except Booker.DoesNotExist:
            return False
        return True

    def has_object_permission(self, request, view, user):
        # Admin can overwrite permission
        if request.user.is_superuser:
            return True

        try:
            booker = Booker.objects.get(user=request.user)
        except Booker.DoesNotExist:
            return False
        return True
