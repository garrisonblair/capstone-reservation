from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_object_permission(self, request, view, user):
        """
            Making sure user can only edit its own data or is admin
        """
        return user == request.user.is_staff

