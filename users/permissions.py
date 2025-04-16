from rest_framework import permissions

class IsAdminOrSelf(permissions.BasePermission):
    """
    Custom permission: Only allow access if the request user is an admin
    or the owner of the object.
    """
    def has_object_permission(self, request, view, obj):
        
        return request.user.is_staff or obj == request.user
