from django import forms
from django.contrib.auth.models import User
from .models import Person, Schedule
from django.forms import ModelForm


class PersonForm(ModelForm):

    class Meta:
        model = Person
        fields = [
            'name',
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
    class Meta:
        model = Schedule
        fields = [
            'name',
        ]
