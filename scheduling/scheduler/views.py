from django.shortcuts import render, get_object_or_404, redirect
from .models import Person, ScheduleSchema, Schedule
from django.forms import modelformset_factory
from .forms import PersonForm, ScheduleForm
from .make_schedule import scheduler
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, 'scheduler/index.html', {})


@login_required
def home(request):

    # PersonFormSet = modelformset_factory(Person, fields='__all__')
    if request.method == 'POST':

        # Set the form equal to the filled out PersonForm
        formset = PersonForm(request.POST)

        if formset.is_valid():

            formset.save()

            # Set success message and reset the form to be empty and reload page
            success_msg = 'Employee successfully added'
            formset = PersonForm()

            if request.user.is_superuser:
                return render(request, 'scheduler/home.html', {'success_msg': success_msg, 'formset': formset, 'super': 'super'})

            return render(request, 'scheduler/home.html', {'success_msg': success_msg, 'formset': formset})
    else:

        # Set the form to be empty upon first visit
        formset = PersonForm()

    if request.user.is_superuser:
        return render(request, 'scheduler/home.html', {'formset': formset, 'super': 'super'})

    return render(request, 'scheduler/home.html', {'formset': formset})


@login_required
def person(request, employee_id):

    # Show all the details of the person
    person = get_object_or_404(Person, pk=employee_id)

    return render(request, 'scheduler/employee.html', {'person': person})


@login_required
def employees(request):

    # Show employees in reverse order of number of shifts
    employee_list = Person.objects.order_by('-shifts')

    return render(request, 'scheduler/employees.html', {'employee_list': employee_list})


@login_required
def schedule_schema(request):

    # Show most recent schedule schema
    if ScheduleSchema.objects.exists():
        schedule_schema = ScheduleSchema.objects.order_by('-updated')[0]

        return render(request, 'scheduler/schema.html', {'schedule_schema': schedule_schema})

    error_msg = "There are no schemas. Sorry!"

    return render(request, 'scheduler/schema.html', {'error_msg': error_msg})


@login_required
def make_schedule(request):

    if not request.user.is_superuser:

        return render(request, 'scheduler/make_schedule.html', {'unauthorized': "You are not authorized to use this page."})

    else:

        if not ScheduleSchema.objects.exists():
            formset = ScheduleForm()
            error_msg = "There are no schemas to use! Make a schema first."
            return render(request, 'scheduler/make_schedule.html', {'error_msg': error_msg, 'formset': formset})

        if request.method == 'POST':

            # Make the name
            formset = ScheduleForm(request.POST)

            if formset.is_valid():

                formset.save()
                scheduler()

                # Set success msg and reset form
                success_msg = "Schedule successfully made"
                formset = ScheduleForm()

                return render(request, 'scheduler/make_schedule.html', {'success_msg': success_msg, 'formset': formset})

        else:
            formset = ScheduleForm()

        return render(request, 'scheduler/make_schedule.html', {'formset': formset})
