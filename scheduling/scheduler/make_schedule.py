from .models import Schedule, Person, ScheduleSchema
import re


def scheduler():
    schedule_to_create = Schedule.objects.order_by('-created')[0]
    sorted_employees = sorted(Person.objects.all(),
                              key=Person.calculate_avail_ratio)
    sched_schema_to_use = ScheduleSchema.objects.order_by('-updated')[0]
    bad_name_list = ["id", "created", "updated", "name"]

    # Starts the scheduling section
    for employee in sorted_employees:
        # Copy employee number of shifts so as not to actually change their object's properties
        employee_shifts = employee.shifts
        for name, value in sched_schema_to_use.get_fields():

            """ Checks that it isn't the name property, the shift(value) is 
            required and that the employee has shifts left to assign """
            if (name not in bad_name_list) and (value == "True") and (employee_shifts > 0):
                clean_name_of_shift = re.sub('Driver|Cashier|Bagger', '', name)

                # Check if the employee is available that day
                if getattr(employee, clean_name_of_shift) == True:
                    # Get the old value so it isn't just overwritten
                    old_value_of_sched = getattr(
                        schedule_to_create, clean_name_of_shift)

                    # Check if employee is already assigned this job
                    if employee.name not in old_value_of_sched:

                        # Check if employee can do job, if job is in name, and if job is not in old value (i.e. already assigned)
                        if employee.Driver and 'Driver' in name and 'Driver' not in old_value_of_sched:
                            value_to_insert = old_value_of_sched + \
                                f"| {employee.name} as Driver |"
                            employee_shifts -= 1

                        elif employee.Cashier and 'Cashier' in name and 'Cashier' not in old_value_of_sched:
                            value_to_insert = old_value_of_sched + \
                                f"| {employee.name} as Cashier |"
                            employee_shifts -= 1

                        elif employee.Bagger and 'Bagger' in name and 'Bagger' not in old_value_of_sched:
                            value_to_insert = old_value_of_sched + \
                                f"| {employee.name} as Bagger |"
                            employee_shifts -= 1

                        else:
                            value_to_insert = old_value_of_sched
                    else:
                        value_to_insert = old_value_of_sched

                    # Update schedule with the employee and their position

                    setattr(schedule_to_create,
                            clean_name_of_shift, value_to_insert)
                    schedule_to_create.save()
