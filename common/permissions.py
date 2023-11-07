from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission

from common.constants import Constants


class IsAnonymous(BasePermission):
    """User should be a Admin and Active, check user.role_id.name == 'ADMIN' and user.is_active"""
    """
    Object level permission also added
    Replace admin and super admin with own user permissions
    """

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return True


class IsStaff(BasePermission):
    """
    Object level permission also added
    Replace admin and super admin with own user permissions
    """

    def has_permission(self, request, view):
        if (not isinstance(request.user, AnonymousUser)) and (request.user.role.name.upper() == Constants.STAFF) \
                and request.user.is_active:
            return True


class IsActiveToken(BasePermission):
    """Candidate(User) should be able to get access only on the latest login session"""

    def has_permission(self, request, view):
        if str(request.user.active_token) == str(request.auth):
            return True
        return False
