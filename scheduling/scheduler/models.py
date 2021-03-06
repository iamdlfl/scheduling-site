from django.db import models
from django.utils import timezone

# Create your models here.


class TimeMixin(models.Model):
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        '''Save timestamps on creation and update'''
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(TimeMixin, self).save(*args, **kwargs)


class ScheduleSchema(TimeMixin):
    name = models.TextField(blank=False)
    MondayAMDriver = models.BooleanField(default=False)
    MondayAMCashier = models.BooleanField(default=False)
    MondayPMDriver = models.BooleanField(default=False)
    MondayPMCashier = models.BooleanField(default=False)
    MondayPMBagger = models.BooleanField(default=False)
    TuesdayAMDriver = models.BooleanField(default=False)
    TuesdayAMCashier = models.BooleanField(default=False)
    TuesdayPMDriver = models.BooleanField(default=False)
    TuesdayPMCashier = models.BooleanField(default=False)
    TuesdayPMBagger = models.BooleanField(default=False)
    WednesdayAMDriver = models.BooleanField(default=False)
    WednesdayAMCashier = models.BooleanField(default=False)
    WednesdayPMDriver = models.BooleanField(default=False)
    WednesdayPMCashier = models.BooleanField(default=False)
    WednesdayPMBagger = models.BooleanField(default=False)
    ThursdayAMDriver = models.BooleanField(default=False)
    ThursdayAMCashier = models.BooleanField(default=False)
    ThursdayPMDriver = models.BooleanField(default=False)
    ThursdayPMCashier = models.BooleanField(default=False)
    ThursdayPMBagger = models.BooleanField(default=False)
    FridayAMDriver = models.BooleanField(default=False)
    FridayAMCashier = models.BooleanField(default=False)
    FridayPMDriver = models.BooleanField(default=False)
    FridayPMCashier = models.BooleanField(default=False)
    FridayPMBagger = models.BooleanField(default=False)
    SaturdayAMDriver = models.BooleanField(default=False)
    SaturdayAMCashier = models.BooleanField(default=False)
    SaturdayPMDriver = models.BooleanField(default=False)
    SaturdayPMCashier = models.BooleanField(default=False)
    SaturdayPMBagger = models.BooleanField(default=False)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

    def get_form_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields[4:]]

    def __str__(self):
        return self.name


class Schedule(TimeMixin):
    name = models.TextField(blank=True)
    MondayAM = models.TextField(blank=True)
    MondayPM = models.TextField(blank=True)
    TuesdayAM = models.TextField(blank=True)
    TuesdayPM = models.TextField(blank=True)
    WednesdayAM = models.TextField(blank=True)
    WednesdayPM = models.TextField(blank=True)
    ThursdayAM = models.TextField(blank=True)
    ThursdayPM = models.TextField(blank=True)
    FridayAM = models.TextField(blank=True)
    FridayPM = models.TextField(blank=True)
    SaturdayAM = models.TextField(blank=True)
    SaturdayPM = models.TextField(blank=True)

    def validate_self(self):
        # Returns tuple of a message and field where error occurs (or None)
        for field in self._meta.fields:
            shifts = field.value_to_string(self).split('|')
            names = []
            positions = []
            for shift in shifts:
                if len(shift.split(' ')) > 2:
                    names.append(shift.split(' ')[0])
                    positions.append(shift.split(' ')[2])
            if not len(set(names)) == len(names):
                return False, 'You scheduled someone for two jobs at the same time!', field.name
            if not len(set(positions)) == len(positions):
                return False, 'You scheduled two people for the same position (Driver, Cashier or Bagger)!', field.name
        return True, 'All looks good! Schedule successfully made.', None

    def get_fields(self):
        fields_to_return = []
        for field in self._meta.fields:
            v = field.value_to_string(self)
            if ('AM' in field.name or 'PM' in field.name) and 'Driver' not in v:
                return [('ERROR', ['There appears to be an error with the schedule. Make sure someone is scheduled as a driver for every shift.'])]
            elif '|' in v:
                new_v = v.split('|')
                fields_to_return.append((field.name, new_v))
            else:
                fields_to_return.append((field.name, [v]))
        return fields_to_return

    def get_form_fields(self):
        fields_to_return = []
        for field in self._meta.fields[3:]:
            fields_to_return.append(field.name)
        return fields_to_return


    def __str__(self):
        return self.name
