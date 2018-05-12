from django.db import models
from django.db.models import Count, Sum, Avg
from datetime import datetime
from decimal import Decimal
from djmoney.models.fields import MoneyField
import os
from django.conf import settings
import csv
from django.db.models import Q

def getUploadFileName(instance, filename):
    # return "%s_%s" % (str(datetime().today, filename)
    return (filename[17:])



def parseHoursFile(filepath, wee, west7):
    
    with open(filepath, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='"')
        rows = list(filereader)
        dateRange = rows[1][0].split(' - ')
        strStartDate = dateRange[0]
        strEndDate = dateRange[1]
        

        startDate = datetime.strptime(strStartDate, '%b %d, %Y').date()
        endDate = datetime.strptime(strEndDate, '%b %d, %Y').date()
        print(strStartDate)
        print(endDate)
        weeDays = findAllDays(startDate, endDate, wee)
        west7Days = findAllDays(startDate, endDate, west7)


def getTotalTippableHoursForLocation(e, weekDay, location ):
    if e.first_name=='Ben' and e.last_name=='Villano':
        shifts = e.shift_set.filter(day__week_day= weekDay ).filter(Q(role='Barista/Server') | Q(role='Shift Lead/MOD') | Q(role='Bakery') ).filter(day__location__location= location )
        totalTippableHours = 0
        for shift in shifts:
            # print(shift.day_id.date)
            # print(shift.day_id.week_day)
            # print(shift.day_id.location_id.location)
            # print(shift.hours)
            totalTippableHours += shift.hours
            # print(totalTippableHours)
        return totalTippableHours
    else:
        shifts = e.shift_set.filter(day__week_day= weekDay ).filter(Q(role='Barista/Server') | Q(role='Shift Lead/MOD')).filter(day__location__location= location )
        totalTippableHours = 0
        for shift in shifts:
            # print(shift.day_id.date)
            # print(shift.day_id.week_day)
            # print(shift.day_id.location_id.location)
            # print(shift.hours)
            totalTippableHours += shift.hours
            # print(totalTippableHours)
        return totalTippableHours


# Create your models here.
class Tip(models.Model):
    title = models.CharField(max_length=200)
    wee_sunday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_sunday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_sunday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_sunday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_monday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_monday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_monday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_monday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_tuesday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_tuesday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_tuesday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_tuesday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_wednesday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_wednesday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_wednesday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_wednesday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_thursday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_thursday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_thursday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_thursday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_friday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_friday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_friday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_friday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_saturday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_saturday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_saturday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_saturday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_sunday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_sunday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_sunday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_sunday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    hours_file = models.FileField(upload_to=getUploadFileName)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Tips"

class Employee(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)

    def wee_sun_hours(self):
        return getTotalTippableHoursForLocation(self, 'Sunday', 'Wee Claddagh')

    def west7_sun_hours(self):
        return getTotalTippableHoursForLocation(self, 'Sunday', 'Claddagh Coffee')

    def wee_mon_hours(self):
        return getTotalTippableHoursForLocation(self, 'Monday', 'Wee Claddagh')

    def west7_mon_hours(self):
        return getTotalTippableHoursForLocation(self, 'Monday', 'Claddagh Coffee')

    def wee_tue_hours(self):
        return getTotalTippableHoursForLocation(self, 'Tuesday', 'Wee Claddagh')

    def west7_tue_hours(self):
        return getTotalTippableHoursForLocation(self, 'Tuesday', 'Claddagh Coffee')

    def wee_wed_hours(self):
        return getTotalTippableHoursForLocation(self, 'Wednesday', 'Wee Claddagh')

    def west7_wed_hours(self):
        return getTotalTippableHoursForLocation(self, 'Wednesday', 'Claddagh Coffee')

    def wee_thu_hours(self):
        return getTotalTippableHoursForLocation(self, 'Thursday', 'Wee Claddagh')

    def west7_thu_hours(self):
        return getTotalTippableHoursForLocation(self, 'Thursday', 'Claddagh Coffee')

    def wee_fri_hours(self):
        return getTotalTippableHoursForLocation(self, 'Friday', 'Wee Claddagh')

    def west7_fri_hours(self):
        return getTotalTippableHoursForLocation(self, 'Friday', 'Claddagh Coffee')

    def wee_sat_hours(self):
        return getTotalTippableHoursForLocation(self, 'Saturday', 'Wee Claddagh')

    def west7_sat_hours(self):
        return getTotalTippableHoursForLocation(self, 'Saturday', 'Claddagh Coffee')

    def total_hours(self):
        return self.shift_set.aggregate(Sum('hours'))['hours__sum']


class Location(models.Model):
    location = models.CharField(max_length=30)
    tips = models.ManyToManyField(Tip)
    employees = models.ManyToManyField(Employee)

def getTotalHours(day):
    return day.shift_set.aggregate(Sum('hours'))['hours__sum']

class Day(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateField()
    week_day = models.CharField(max_length=20)
    cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    
    def total_tips(self): 
        return self.cash_tips + self.cred_tips

    def total_hours(self):
        return self.shift_set.aggregate(Sum('hours'))['hours__sum']


        

class Shift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    times = models.CharField(max_length = 50)
    role = models.CharField(max_length = 40)
    hours = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0000.00'))






