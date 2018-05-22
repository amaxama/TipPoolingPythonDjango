from django.db import models
from django.core.validators import FileExtensionValidator
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

def getTotalTippableHoursForLocation(e, weekDay, location ):
    if e.first_name=='Ben' and e.last_name=='Villano':
        shifts = e.shift_set.filter(day__week_day= weekDay ).filter(Q(role='Barista/Server') | Q(role='Shift Lead/MOD') | Q(role='Bakery') ).filter(day__location__location= location )
        totalTippableHours = 0
        for shift in shifts:
            totalTippableHours += shift.hours
        return totalTippableHours
    else:
        shifts = e.shift_set.filter(day__week_day= weekDay ).filter(Q(role='Barista/Server') | Q(role='Shift Lead/MOD')).filter(day__location__location= location )
        totalTippableHours = 0
        for shift in shifts:
            totalTippableHours += shift.hours
        return totalTippableHours


# Create your models here.
class Tip(models.Model):
    title = models.DateField()
    wee_Sunday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_Sunday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_Sunday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_Sunday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_Monday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_Monday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_Monday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_Monday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_Tuesday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_Tuesday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_Tuesday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_Tuesday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_Wednesday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_Wednesday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_Wednesday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_Wednesday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_Thursday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_Thursday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_Thursday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_Thursday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_Friday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_Friday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_Friday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_Friday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_Saturday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_Saturday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_Saturday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_Saturday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_Sunday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_Sunday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_Sunday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_Sunday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    # created_at = models.DateTimeField(default=datetime.now, blank=True)
    hours_file = models.FileField(upload_to=getUploadFileName, validators = [FileExtensionValidator(['csv'])])

    def __str__(self):
        try:
            return self.title.strftime('%b %d, %Y')
        except:
            return "Tip try"
    class Meta:
        verbose_name_plural = "Tips"

    def getCashTips(self, location, weekDay):
        cashTips = {'Wee Claddagh': {'Sunday': self.wee_Sunday_cash_tips, 'Monday': self.wee_Monday_cash_tips, 'Tuesday': self.wee_Tuesday_cash_tips, 'Wednesday': self.wee_Wednesday_cash_tips, 'Thursday': self.wee_Thursday_cash_tips, 'Friday': self.wee_Friday_cash_tips, 'Saturday': self.wee_Saturday_cash_tips}, 'Claddagh Coffee': {'Sunday': self.west7_Sunday_cash_tips, 'Monday': self.west7_Monday_cash_tips, 'Tuesday': self.west7_Tuesday_cash_tips, 'Wednesday': self.west7_Wednesday_cash_tips, 'Thursday': self.west7_Thursday_cash_tips, 'Friday': self.west7_Friday_cash_tips, 'Saturday': self.west7_Saturday_cash_tips}}
        return cashTips[location][weekDay]

    def getCredTips(self, location, weekDay):
        credTips = {'Wee Claddagh': {'Sunday': self.wee_Sunday_cred_tips, 'Monday': self.wee_Monday_cred_tips, 'Tuesday': self.wee_Tuesday_cred_tips, 'Wednesday': self.wee_Wednesday_cred_tips, 'Thursday': self.wee_Thursday_cred_tips, 'Friday': self.wee_Friday_cred_tips, 'Saturday': self.wee_Saturday_cred_tips}, 'Claddagh Coffee': {'Sunday': self.west7_Sunday_cred_tips, 'Monday': self.west7_Monday_cred_tips, 'Tuesday': self.west7_Tuesday_cred_tips, 'Wednesday': self.west7_Wednesday_cred_tips, 'Thursday': self.west7_Thursday_cred_tips, 'Friday': self.west7_Friday_cred_tips, 'Saturday': self.west7_Saturday_cred_tips}}
        return credTips[location][weekDay]


class Employee(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)

    def wee_sun_hours(self):
        return getTotalTippableHoursForLocation(self, 'Sunday', 'Wee Claddagh')

    def wee_sun_cash_tips(self):
        hours = getTotalTippableHoursForLocation(self, 'Sunday', 'Wee Claddagh')

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

    def wee_total_hours(self):
        return self.shift_set.filter(day__location__location = 'Wee Claddagh').filter(Q(role='Barista/Server') | Q(role='Shift Lead/MOD') | Q(role='Bakery')).exclude(employee__first_name = 'Anna', role = 'Bakery').aggregate(Sum('hours'))['hours__sum']

    def west7_total_hours(self):
        return self.shift_set.filter(day__location__location = 'Claddagh Coffee').filter(Q(role='Barista/Server') | Q(role='Shift Lead/MOD') | Q(role='Bakery')).exclude(employee__first_name = 'Anna', role = 'Bakery').aggregate(Sum('hours'))['hours__sum']


class Location(models.Model):
    location = models.CharField(max_length=30)
    tips = models.ManyToManyField(Tip)
    employees = models.ManyToManyField(Employee)

class Day(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateField()
    week_day = models.CharField(max_length=20)
    cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')

    def total_tips(self): 
        return self.cash_tips + self.cred_tips

    def total_hours(self):
        return self.shift_set.filter(Q(role='Barista/Server') | Q(role='Shift Lead/MOD') | Q(role='Bakery')).exclude(employee__first_name = 'Anna', role = 'Bakery').aggregate(Sum('hours'))['hours__sum']

    @property
    def cash_tips_per_hour(self):
        total_hours = self.shift_set.filter(Q(role='Barista/Server') | Q(role='Shift Lead/MOD') | Q(role='Bakery')).exclude(employee__first_name = 'Anna', role = 'Bakery').aggregate(Sum('hours'))['hours__sum']
        if total_hours != None:
            return (self.cash_tips / total_hours)
        else:
            return 0

    @property
    def cred_tips_per_hour(self):
        total_hours = self.shift_set.filter(Q(role='Barista/Server') | Q(role='Shift Lead/MOD') | Q(role='Bakery')).exclude(employee__first_name = 'Anna', role = 'Bakery').aggregate(Sum('hours'))['hours__sum']
        if total_hours != None:
            return (self.cred_tips / total_hours)
        else:
            return 0
        

    @property
    def total_tips_per_hour(self):
        total_tips = self.cash_tips + self.cred_tips
        total_hours = self.shift_set.filter(Q(role='Barista/Server') | Q(role='Shift Lead/MOD') | Q(role='Bakery')).exclude(employee__first_name = 'Anna', role = 'Bakery').aggregate(Sum('hours'))['hours__sum']
        if total_hours != None:
            return total_tips / total_hours
        else:
            return 0


        

class Shift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    times = models.CharField(max_length = 50)
    role = models.CharField(max_length = 40)
    hours = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0000.00'))








