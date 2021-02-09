from django.shortcuts import render, get_object_or_404, redirect
from .models import ScheduleSchema, Schedule
from django.forms import modelformset_factory
from .forms import PersonForm, ScheduleForm, ManualScheduleForm
from .make_schedule import scheduler
from django.contrib.auth.decorators import login_required
from users.models import Person
from .utils import sort_positions

# Create your views here.


@login_required
def home(request):
    emp_names = [p.username for p in Person.objects.filter(
        groups__name__in=['Employee'])]

    if Schedule.objects.exists():
        # Get the most recent schedule
        sched = Schedule.objects.order_by('-updated')[0]

        if request.user.is_staff:
            return render(request, 'scheduler/home.html', {'staff': 'staff', 'sched': sched})

        return render(request, 'scheduler/home.html', {'sched': sched})

    if request.user.is_staff:
        return render(request, 'scheduler/home.html', {'staff': 'staff'})

    msg = "There doesn't appear to be a schedule ready. Contact Nelson!"

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

    # emp_names = [p.username for p in Person.objects.filter(
    #     groups__name__in=['Employee'])]

    # Show most recent schedule schema
    if ScheduleSchema.objects.exists():
        schedule_schema = ScheduleSchema.objects.order_by('-updated')[0]

        return render(request, 'scheduler/schema.html', {'schedule_schema': schedule_schema})

    error_msg = "There are no schemas. Sorry!"

    return render(request, 'scheduler/schema.html', {'error_msg': error_msg})

@login_required
def manually_make_schedule(request):

    if not request.user.is_staff:

        return render(request, 'scheduler/manually_make_schedule.html', {'unauthorized': "You are not authorized to use this page."})

    else:
        employee_list = Person.objects.filter(
            groups__name__in=['Employee']).order_by('username')
        # To use in the bootstrap columns
        columns = int(12/(len(employee_list) + 1))

        if not ScheduleSchema.objects.exists():
            error_msg = "There are no schemas to use! Make a schema first."
            return render(request, 'scheduler/manually_make_schedule.html', {'error_msg': error_msg, 'employees': employee_list})
            
        fields = Schedule.get_form_fields(Schedule)

        if request.method == 'POST':
            # Get the form data
            data = dict(request.__dict__['_post'])
            new_data = {}
            for k, v in data.items():
                # Clean up form data and sort it
                while 'None' in v:
                    v.remove('None')
                if len(v) > 1:
                    v = sorted(v, reverse=True, key=sort_positions)
                new_data[k]=v
            # Create schedule
            new_schedule = Schedule(
                name=new_data['name'][0],
                MondayAM='|'.join(new_data['MondayAM']),
                MondayPM='|'.join(new_data['MondayPM']),
                TuesdayAM='|'.join(new_data['TuesdayAM']),
                TuesdayPM='|'.join(new_data['TuesdayPM']),
                WednesdayAM='|'.join(new_data['WednesdayAM']),
                WednesdayPM='|'.join(new_data['WednesdayPM']),
                ThursdayAM='|'.join(new_data['ThursdayAM']),
                ThursdayPM='|'.join(new_data['ThursdayPM']),
                FridayAM='|'.join(new_data['FridayAM']),
                FridayPM='|'.join(new_data['FridayPM']),
                SaturdayAM='|'.join(new_data['SaturdayAM']),
                SaturdayPM='|'.join(new_data['SaturdayPM']),
            )

            # Need to do error checking here!!
            valid, msg, field_name = new_schedule.validate_self()
            if not valid:
                error_msg = f'{msg} The error looks like it took place in the {field_name} field.'
                schedule = new_schedule
                return render(request, 'scheduler/manually_make_schedule.html', {'error_msg': error_msg, 'fields': fields, 'employees': employee_list, 'columns': columns, 'schedule': schedule})


            new_schedule.save()
            success_msg = msg
            schedule = Schedule.objects.order_by('-updated')[0]
            return render(request, 'scheduler/manually_make_schedule.html', {'success_msg': success_msg, 'fields': fields, 'employees': employee_list, 'columns': columns, 'schedule': schedule})

        else:
            if Schedule.objects.exists():
                # Eventually use this to populate the fields with the last schedule to make it easier.
                schedule = Schedule.objects.order_by('-updated')[0]
                return render(request, 'scheduler/manually_make_schedule.html', {'fields': fields, 'employees': employee_list, 'columns': columns, 'schedule': schedule})
            return render(request, 'scheduler/manually_make_schedule.html', {'fields': fields, 'employees': employee_list, 'columns': columns})


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

                # Set schedule equal to last schedule
                if ('repeat' in request.__dict__['_post']) and Schedule.objects.exists():
                    sched = Schedule.objects.order_by('-updated')[0]
                    sched.name = formset.cleaned_data.get('name')
                    sched.pk = None
                    sched.save()
                elif ('repeat' in request.__dict__['_post']) and not Schedule.objects.exists():
                    formset = ScheduleForm()
                    error_msg = "There is no past schedule to repeat. Create a new schedule without selecting that box."
                    return render(request, 'scheduler/make_schedule.html', {'error_msg': error_msg, 'formset': formset})

                else:
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
def my_schedule(request):
    if Person.objects.filter(username=request.user).exists() and Schedule.objects.exists():
        # Get the most recent schedule and the Person
        sched = Schedule.objects.order_by('-updated')[0]
        instance = get_object_or_404(Person, username=request.user)
        info = []
        for name, value in sched.get_fields():
            for v in value:
                if instance.username in v:
                    info.append((name, v.strip().split(' ')[2]))


        return render(request, 'scheduler/my_schedule.html', {'info': info, 'user': instance})

    return render(request, 'scheduler/my_schedule.html')


@login_required
def change_avail(request):

    if Person.objects.filter(username=request.user).exists():

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

    return render(request, 'scheduler/change_avail.html', {})
