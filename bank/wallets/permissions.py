from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    '''Custom permission to only allow owners to create object'''

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner or request.user.is_staff:
            return True
