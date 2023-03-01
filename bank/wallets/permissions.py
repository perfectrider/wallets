from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    '''Custom permission to only allow owners to create object'''

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner or request.user.is_staff:
            return True

    # def has_object_permission(self, request, view, obj):
    #     # Read permissions are allowed to any request,
    #     # so we'll always allow GET, HEAD or OPTIONS requests.
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #
    #     # Instance must have an attribute named `owner`.
    #     return obj.user == request.user