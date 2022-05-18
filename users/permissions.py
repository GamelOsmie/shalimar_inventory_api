from rest_framework.permissions import BasePermission


class AdminsOnly(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "Super Admin" or "Admin":
            return False
        return True
