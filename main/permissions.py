from models import CmsUser
from rest_framework.permissions import IsAuthenticated


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