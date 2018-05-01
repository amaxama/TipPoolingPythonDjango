from django.db import models
from datetime import datetime
from time import time
from money.money import Money
from money.currency import Currency 
from decimal import Decimal
from djmoney.models.fields import MoneyField

def getUploadFileName(instance, filename):
    # return "%s_%s" % (str(datetime().today, filename)
    return (filename[17:])

# Create your models here.
class Tips(models.Model):
    title = models.CharField(max_length=200)
    wee_Mon_Cash_Tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    wee_Mon_Cred_Tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    w7_Mon_Cash_Tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    w7_Mon_Cred_Tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    tuesCashTips = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.0000'))
    tuesCredTips = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.0000'))
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    hours_File = models.FileField(upload_to=getUploadFileName)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Tips"