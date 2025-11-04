from rest_framework import permissions
from .models import Permission, ResourceType, Action, UserPermission, UserRole


class HasPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        resource_type_name = getattr(view, 'resource_type', None)
        action_name = getattr(view, 'action_name', None)

        if not resource_type_name or not action_name:
            return False

        try:
            permission = Permission.objects.get(
                resource_type__name=resource_type_name,
                action__name=action_name
            )

            has_perm = (
                    UserPermission.objects.filter(
                        user=request.user,
                        permission=permission
                    ).exists() or
                    UserRole.objects.filter(
                        user=request.user,
                        role__permissions=permission
                    ).exists()
            )

            return has_perm

        except Permission.DoesNotExist:
            return False


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
