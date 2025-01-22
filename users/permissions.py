from rest_framework import permissions

class RoleBasedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        # Define role-based permissions
        if request.user.role == 'ADMIN':
            return True
            
        if request.user.role == 'DIRECTOR':
            # Add specific permissions for directors
            return True
            
        if request.user.role == 'DHR':
            # Add specific permissions for DHR
            return True

        if request.user.role in ['STAFF', 'TEACHER', 'STUDENT', 'PARENT', 'LIBRARIAN', 'ACCOUNTANT', 'STOREKEEPER']:
            # Add specific permissions for other roles
            return True

        return False