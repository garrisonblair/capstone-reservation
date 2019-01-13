from rest_framework.permissions import BasePermission
from apps.accounts.models.BookerProfile import BookerProfile


class IsBooker(BasePermission):
    def has_permission(self, request, view):
        # Admin can overwrite permission
        if request.user.is_superuser:
            return True

        try:
            booker = BookerProfile.objects.get(user=request.user)
        except BookerProfile.DoesNotExist:
            return False
        return True

    def has_object_permission(self, request, view, user):
        # Admin can overwrite permission
        if request.user.is_superuser:
            return True

        try:
            booker = BookerProfile.objects.get(user=request.user)
        except BookerProfile.DoesNotExist:
            return False
        return True
