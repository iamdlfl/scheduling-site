from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.TextField(blank=False)
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
    shifts = models.IntegerField(blank=False)
    flex = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def calculate_avail_ratio(self):
        """Returns a value calculating how 'available' someone is"""
        shifts_avail = 0
        jobs_can_do = 0
        if self.Bagger == True: jobs_can_do += 1
        if self.Cashier == True: jobs_can_do += 1
        if self.Driver == True: jobs_can_do += 1
        for k, v in self.__dict__.items():
            if k == 'shifts':
                continue
            elif v == 1:
                shifts_avail += v
        ratio = 1 / ((self.shifts * jobs_can_do) / shifts_avail)
        return ratio    

class ScheduleSchema(models.Model):
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

    def __str__(self):
        return self.name

class Schedule(models.Model):
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

    def __str__(self):
        return self.name
