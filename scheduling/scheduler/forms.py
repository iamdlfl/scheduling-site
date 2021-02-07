from django import forms
from django.contrib.auth.models import User
from .models import Schedule
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from users.forms import UserRegisterForm
from users.models import Person


class PersonForm(ModelForm):

    class Meta:
        model = Person
        fields = [
            'MondayAM',
            'MondayPM',
            'TuesdayAM',
            'TuesdayPM',
            'WednesdayAM',
            'WednesdayPM',
            'ThursdayAM',
            'ThursdayPM',
            'FridayAM',
            'FridayPM',
            'SaturdayAM',
            'SaturdayPM',
            'Driver',
            'Cashier',
            'Bagger',
            'shifts',
            'flex',
        ]


class ScheduleForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'name',
            'id': 'name'
        }))

    class Meta:
        model = Schedule
        fields = [
            'name',
        ]

class ManualScheduleForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'name',
            'id': 'name'
        }
    ))
    class Meta:
        model = Schedule
        fields = [
            "name",
            "MondayAM",
            "MondayPM",
            "TuesdayAM",
            'TuesdayPM',
            'WednesdayAM',
            'WednesdayPM',
            'ThursdayAM',
            'ThursdayPM',
            'FridayAM',
            'FridayPM',
            'SaturdayAM',
            'SaturdayPM'
        ]
