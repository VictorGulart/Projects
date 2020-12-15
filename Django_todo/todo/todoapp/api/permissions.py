# creating custom permissions
from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsOwnerOrReadOnly(BasePermission):
    '''
    Only allows owners to edit things
    '''

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Instance must have an attribute named owner
        return obj.owner == request.user

