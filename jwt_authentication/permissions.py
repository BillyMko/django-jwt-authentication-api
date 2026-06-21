from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user and
                request.user.is_authenticated and
                request.user.role == "admin"
                )
    
class IsPremium(BasePermission):
    def has_permission(self, request, view):
        return (request.user and
                request.user.is_authenticated and
                getattr(request.user, "role", None) in ("admin", "premium")
                )
    
class IsOwnerOrAdmin(BasePermission):
   def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        
        if hasattr(obj, "user"):
            return (obj.user == request.user)
        
        return obj == request.user 