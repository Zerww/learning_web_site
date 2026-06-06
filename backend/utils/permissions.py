"""Custom permissions."""
from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """Allow access only to admin users (role=1)."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 1)


class IsOwnerOrAdmin(BasePermission):
    """Allow access to object owner or admin."""

    def has_object_permission(self, request, view, obj):
        if request.user.role == 1:
            return True
        if hasattr(obj, 'user_id'):
            return obj.user_id == request.user.id
        if hasattr(obj, 'author_id'):
            return obj.author_id == request.user.id
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'author'):
            return obj.author == request.user
        return False


class IsOwnerOrAdminForComment(BasePermission):
    """Allow comment owner or admin to delete/update."""

    def has_object_permission(self, request, view, obj):
        if request.user.role == 1:
            return True
        return obj.user_id == request.user.id
