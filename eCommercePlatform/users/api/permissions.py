from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        READ permission are allowed to any request,
        so always allow GET, HEAD or OPTIONS requests.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return permissions.IsAdminUser.has_permission(self, request, view)
