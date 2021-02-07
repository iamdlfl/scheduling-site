from .models import Schedule, ScheduleSchema
from users.models import Person
import re
import operator

BAD_NAME_LIST = ["id", "created", "updated", "name"]


def sort_shifts(schedule_schema_to_sort, list_of_employees):
    """Sorts the list of shifts by how many employees can work that job

    :param schedule_schema_to_sort: The schema that you want to sort, it should just be 'sched_schema_to_use' in the below scheduler() function
    :param list_of_employees: A list of employees to check, it should just be sorted_employees below
    :return list_of_shift_names: Returns the sorted list of shifts names
    """

    temp_dict = {}
    for name, value in schedule_schema_to_sort.get_fields():
        if name not in BAD_NAME_LIST:
            if "AM" in name:
                index = name.index("AM")
            elif "PM" in name:
                index = name.index("PM")
            job = name[index+2:]
            shift_name = name[:index+2]
            counter = 0
            for employee in list_of_employees:
                if getattr(employee, shift_name) and getattr(employee, job):
                    counter += 1
            if counter != 0:
                temp_dict[name] = counter
    temp_list = sorted(temp_dict.items(), key=operator.itemgetter(1))
    list_of_shift_names = [tup[0] for tup in temp_list]
    return list_of_shift_names


def scheduler():
    schedule_to_create = Schedule.objects.order_by('-created')[0]
    sorted_employees = sorted(Person.objects.all(),
                              key=Person.calculate_avail_ratio)
    sched_schema_to_use = ScheduleSchema.objects.order_by('-updated')[0]

    sorted_shifts = sort_shifts(sched_schema_to_use, sorted_employees)

    # Starts the scheduling section
    for employee in sorted_employees:
        # Copy employee number of shifts so as not to actually change their object's properties
        employee_shifts = employee.shifts

        for name in sorted_shifts:

            # Checks that it isn't the name property, the shift(value) is
            # required and that the employee has shifts left to assign
            if (name not in BAD_NAME_LIST) and (getattr(sched_schema_to_use, name)) and (employee_shifts > 0):
                clean_name_of_shift = re.sub('Driver|Cashier|Bagger', '', name)

                # Check if the employee is available that day
                if getattr(employee, clean_name_of_shift) == True:
                    # Get the old value so it isn't just overwritten
                    old_value_of_sched = getattr(
                        schedule_to_create, clean_name_of_shift)
                    

                    # Check if employee is already assigned this job
                    if employee.username not in old_value_of_sched:

                        # Check if employee can do job, if job is in name, and if job is not in old value (i.e. already assigned)
                        if employee.Driver and 'Driver' in name and 'Driver' not in old_value_of_sched:
                            if (old_value_of_sched == ''):
                                value_to_insert = old_value_of_sched + \
                                    f" {employee.username} as Driver "
                            else:
                                value_to_insert = f"{employee.username} as Driver |" + old_value_of_sched
                            employee_shifts -= 1

                        elif employee.Cashier and 'Cashier' in name and 'Cashier' not in old_value_of_sched:
                            if (old_value_of_sched == ''):
                                value_to_insert = old_value_of_sched + \
                                    f" {employee.username} as Cashier "
                            else:
                                value_to_insert = old_value_of_sched + \
                                    f"| {employee.username} as Cashier "
                            employee_shifts -= 1

                        elif employee.Bagger and 'Bagger' in name and 'Bagger' not in old_value_of_sched:
                            if (old_value_of_sched == ''):
                                value_to_insert = old_value_of_sched + \
                                    f" {employee.username} as Bagger "
                            else:
                                value_to_insert = old_value_of_sched + \
                                    f"| {employee.username} as Bagger "
                            employee_shifts -= 1

                        else:
                            value_to_insert = old_value_of_sched
                    else:
                        value_to_insert = old_value_of_sched

                    # Update schedule with the employee and their position

                    setattr(schedule_to_create,
                            clean_name_of_shift, value_to_insert)
                    schedule_to_create.save()
