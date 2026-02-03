from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    '''Serializer for User model to expose id, username, and role fields.'''
    class Meta:
        model = User
        fields = ['id', 'username', 'role']
