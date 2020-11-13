from django.contrib import admin
from .models import Person
# Register your models here.

# admin.site.register(Person)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    exclude = (
        'password',
        'is_active',
        'is_staff',
        'first_name',
        'last_name',
        'email',
        'date_joined',
        'is_superuser',
        'created',
        'updated',
        'user_permissions',
    )
    list_display = (
        'username',
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
    )
