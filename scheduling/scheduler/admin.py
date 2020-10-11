from django.contrib import admin

from .models import Person, ScheduleSchema, Schedule
# Register your models here.

admin.site.register(Person)
admin.site.register(ScheduleSchema)
admin.site.register(Schedule)
