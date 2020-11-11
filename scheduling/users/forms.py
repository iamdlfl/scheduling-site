from django import forms
from .models import Person
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = Person

        fields = [
            'username',
            'password1',
            'password2'
        ]
