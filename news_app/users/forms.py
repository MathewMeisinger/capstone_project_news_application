from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    '''
    Custom user registration form that includes a role selection.
    Allows users to select their role during registration.
    Requires 'username', 'email', 'role', 'password1', and 'password2' fields.
    '''
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
