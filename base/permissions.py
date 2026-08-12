from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    massage = 'You are not the owner of this object'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsBarber(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'barber'


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'
