from models import CmsUser
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions


class IsAppUser(IsAuthenticated):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        permission = super(IsAppUser, self).has_permission(request, view)
        try:
            return permission and request.user is not None
        except CmsUser.DoesNotExist:
            return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user