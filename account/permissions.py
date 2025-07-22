from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_customer()

class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin():
            return True
        if request.user.is_customer():
            return obj.user == request.user
        return False

    def has_permission(self, request, view):
        return request.user.is_authenticated
