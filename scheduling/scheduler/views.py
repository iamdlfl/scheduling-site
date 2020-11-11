from django.shortcuts import render, get_object_or_404, redirect
from .models import ScheduleSchema, Schedule
from django.forms import modelformset_factory
from .forms import PersonForm, ScheduleForm
from .make_schedule import scheduler
from django.contrib.auth.decorators import login_required
from users.models import Person

# Create your views here.


@login_required
def home(request):
    emp_names = [p.username for p in Person.objects.filter(
        groups__name__in=['Employee'])]

    if (request.user.username in emp_names) and Schedule.objects.exists():
        sched = Schedule.objects.order_by('-updated')[0]

        if request.user.is_staff:
            return render(request, 'scheduler/home.html', {'staff': 'staff', 'sched': sched})

        return render(request, 'scheduler/home.html', {'sched': sched})

    else:
        msg = "You are not listed as an employee yet. Please contact the system administrator."

    if request.user.is_staff:
        return render(request, 'scheduler/home.html', {'staff': 'staff'})

    return render(request, 'scheduler/home.html', {'msg': msg})


@login_required
def employees(request):

    if not request.user.is_staff:

        return render(request, 'scheduler/employees.html', {'unauthorized': "You are not authorized to use this page."})

    # Show employees in reverse order of number of shifts
    employee_list = Person.objects.filter(
        groups__name__in=['Employee']).order_by('-shifts')

    return render(request, 'scheduler/employees.html', {'employee_list': employee_list})


@login_required
def schedule_schema(request):

    emp_names = [p.username for p in Person.objects.filter(
        groups__name__in=['Employee'])]

    # Show most recent schedule schema
    if (request.user.username in emp_names) and ScheduleSchema.objects.exists():
        schedule_schema = ScheduleSchema.objects.order_by('-updated')[0]

        return render(request, 'scheduler/schema.html', {'schedule_schema': schedule_schema})

    error_msg = "There are no schemas. Sorry!"

    if (request.user.username not in emp_names):
        error_msg = "You are not listed as an employee yet. Please contact the system administrator."

    return render(request, 'scheduler/schema.html', {'error_msg': error_msg})


@login_required
def make_schedule(request):

    if not request.user.is_staff:

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


@login_required
def change_avail(request):

    instance = get_object_or_404(Person, username=request.user)

    # PersonFormSet = modelformset_factory(Person, fields='__all__')
    if request.method == 'POST':

        # Set the form equal to the filled out PersonForm
        formset = PersonForm(request.POST, instance=instance)

        if formset.is_valid():

            print(request.user)
            formset.username = request.user
            formset.save()

            # Set success message and reset the form to be empty and reload page
            success_msg = 'Employee successfully changed'
            formset = PersonForm(instance=instance)

            if request.user.is_staff:
                return render(request, 'scheduler/change_avail.html', {'success_msg': success_msg, 'formset': formset, 'staff': 'staff'})

            return render(request, 'scheduler/change_avail.html', {'success_msg': success_msg, 'formset': formset})
    else:

        # Set the form to be normal upon first visit
        formset = PersonForm(instance=instance)

    return render(request, 'scheduler/change_avail.html', {'formset': formset})
