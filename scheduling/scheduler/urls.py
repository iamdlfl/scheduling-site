from django.urls import path
from .views import index, person, employees

urlpatterns = [
    path('', index, name='index'),
    path('employees/<int:employee_id>/', person, name="person"),
    path('employees/', employees, name="employees")
]