from django.db import models
from django.contrib.auth.models import User
from scheduler.models import TimeMixin
# Create your models here.


class Person(TimeMixin, User):
    MondayAM = models.BooleanField(default=False)
    MondayPM = models.BooleanField(default=False)
    TuesdayAM = models.BooleanField(default=False)
    TuesdayPM = models.BooleanField(default=False)
    WednesdayAM = models.BooleanField(default=False)
    WednesdayPM = models.BooleanField(default=False)
    ThursdayAM = models.BooleanField(default=False)
    ThursdayPM = models.BooleanField(default=False)
    FridayAM = models.BooleanField(default=False)
    FridayPM = models.BooleanField(default=False)
    SaturdayAM = models.BooleanField(default=False)
    SaturdayPM = models.BooleanField(default=False)
    Driver = models.BooleanField(default=False)
    Cashier = models.BooleanField(default=False)
    Bagger = models.BooleanField(default=False)
    shifts = models.IntegerField(blank=False, default=0)
    flex = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

    def calculate_avail_ratio(self):
        """Returns a value calculating how 'available' someone is"""
        shifts_avail = 0
        jobs_can_do = 0

        # Add up how many jobs they can perform
        if self.Bagger == True:
            jobs_can_do += 1
        if self.Cashier == True:
            jobs_can_do += 1
        if self.Driver == True:
            jobs_can_do += 1

        # Add up how many shifts they are available
        for k, v in self.__dict__.items():
            if (k.endswith('AM') or k.endswith('PM')) and v == True:
                shifts_avail += 1

        # If they are available at all calculate the ratio, else return 0
        if shifts_avail != 0:
            ratio = ((self.shifts * jobs_can_do) / shifts_avail)
            return ratio
        return 0
