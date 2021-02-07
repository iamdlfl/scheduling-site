from django.urls import path
from .views import (home,
                    employees,
                    schedule_schema,
                    make_schedule,
                    change_avail,
                    my_schedule,
                    manually_make_schedule)


app_name = 'scheduler'
urlpatterns = [
    path('', home, name="home"),
    path('employees/', employees, name="employees"),
    path('schema/', schedule_schema, name="schema"),
    path('schedule/', make_schedule, name="make_schedule"),
    path('change/', change_avail, name="change"),
    path('my_schedule/', my_schedule, name="my_schedule"),
    path('manual_schedule/', manually_make_schedule, name="manually_make_schedule"),
]
