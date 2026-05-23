from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="admin").exists()


class IsOperator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="operator").exists()


class IsViewer(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="viewer").exists()


class IsAdminOrOperator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=["admin", "operator"]).exists()