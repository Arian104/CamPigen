from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Allows access only to admin users"""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsOrganizationMember(permissions.BasePermission):
    """Allows access only to members of the organization"""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admin can access everything
        if request.user.is_staff:
            return True
        
        # Check organization access
        org_id = request.headers.get('X-Organization-ID')
        if org_id:
            return str(request.user.profile.organization_id) == org_id
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        # Check if object belongs to user's organization
        if hasattr(obj, 'organization'):
            return obj.organization_id == request.user.profile.organization_id
        return True

class IsAdminOrReadOnly(permissions.BasePermission):
    """Admin can do anything, others can only read"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
