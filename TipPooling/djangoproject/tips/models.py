from django.db import models

from datetime import datetime
from decimal import Decimal
from djmoney.models.fields import MoneyField
import os
from django.conf import settings
import csv

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

# Create your models here.
class Tip(models.Model):
    title = models.CharField(max_length=200)
    wee_monday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_monday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_monday_cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    west7_monday_cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    hours_file = models.FileField(upload_to=getUploadFileName)


    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Tips"

class Location(models.Model):
    location = models.CharField(max_length=30)
    tips = models.ManyToManyField(Tip)

class Day(models.Model):
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateField()
    week_day = models.CharField(max_length=20)
    cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')

class Employee(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    total_hours = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal('000.000'))

class Shift(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    day_id = models.ForeignKey(Day, on_delete=models.CASCADE)
    times = models.CharField(max_length = 50)
    role = models.CharField(max_length = 40)
    hours = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0000.00'))






