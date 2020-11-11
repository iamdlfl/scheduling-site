from django.urls import path
from .views import (home,
                    employees,
                    schedule_schema,
                    make_schedule,
                    change_avail)


app_name = 'scheduler'
urlpatterns = [
    path('', home, name="home"),
    path('employees/', employees, name="employees"),
    path('schema/', schedule_schema, name="schema"),
    path('schedule/', make_schedule, name="make_schedule"),
    path('change/', change_avail, name="change"),
]
