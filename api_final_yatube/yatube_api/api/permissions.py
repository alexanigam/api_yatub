from rest_framework import permissions


class OnlyOwnerCanModify(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS', 'POST'):
            return True
        return obj.author == request.user
