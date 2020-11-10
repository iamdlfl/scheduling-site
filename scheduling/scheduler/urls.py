from django.urls import path
from .views import (home,
                    person,
                    employees,
                    schedule_schema,
                    make_schedule,
                    index)


app_name = 'scheduler'
urlpatterns = [
    path('', index, name="index"),
    path('home/', home, name="home"),
    path('employee/<int:employee_id>/', person, name="employee"),
    path('employees/', employees, name="employees"),
    path('schema/', schedule_schema, name="schema"),
    path('schedule/', make_schedule, name="make_schedule")
]
