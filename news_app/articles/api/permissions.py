from rest_framework.permissions import BasePermission


class IsJournalist(BasePermission):
    '''
    Custom permission to only allow users with the 'journalist' role to create
    or modify articles.
    '''
    def has_permission(self, request, view):
        return request.user.role == 'journalist'


class IsEditor(BasePermission):
    '''
    Custom permission to only allow users with the 'editor' role to approve
    articles.
    '''
    def has_permission(self, request, view):
        return request.user.role == 'editor'


class IsAuthorOrEditor(BasePermission):
    '''
    Custom permission to allow authors to edit their own articles and editors
    to approve articles.
    '''
    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'editor' or
            obj.author == request.user
        )
