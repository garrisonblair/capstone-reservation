from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, user):
        """
            Making sure user can only edit its own data or is admin
        """
        return user == request.user or request.user.is_staff
