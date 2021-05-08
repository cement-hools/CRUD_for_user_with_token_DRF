from rest_framework import permissions


class ProjectPermission(permissions.BasePermission):
    """Права для проекта."""

    def has_permission(self, request, view):
        return bool(
            (request.method in ('GET', 'PUT', 'DELETE'))
            or (request.user.is_staff and request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            (request.method in permissions.SAFE_METHODS)
            or (obj == request.user)
            or (request.user.is_staff)
        )
