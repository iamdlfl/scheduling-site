from django.contrib import admin

from .models import ScheduleSchema, Schedule
# Register your models here.

admin.site.register(ScheduleSchema)
admin.site.register(Schedule)
