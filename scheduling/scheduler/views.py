from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Person


# Create your views here.

def index(request): 
    return render(request, 'scheduler/index.html')

def person(request, employee_id):
    try:
        response = f"You're looking at {Person.objects.get(pk=employee_id)}'s page."
        return HttpResponse(response)
    except Person.DoesNotExist:
        raise Http404("This person or employee ID does not exist.")
    except:
        raise Http404("An unkown error has occured. Please contact the site administrator.")

def employees(request):
    employee_list = Person.objects.order_by('-shifts')
    template = loader.get_template('scheduler/employees.html')
    context = {
        'employee_list': employee_list
    }
    return HttpResponse(template.render(context, request))