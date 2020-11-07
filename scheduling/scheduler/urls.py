from django.urls import path
from .views import (index,
                    person,
                    employees,
                    schedule_schema,
                    make_schedule,
                    login)


app_name = 'scheduler'
urlpatterns = [
    path('', login, name="login"),
    path('index/', index, name="index"),
    path('employees/<int:employee_id>/', person, name="employee"),
    path('employees/', employees, name="employees"),
    path('schema/', schedule_schema, name="schema"),
    path('schedule/', make_schedule, name="make_schedule")
]
