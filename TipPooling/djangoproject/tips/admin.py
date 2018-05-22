from django import forms
from django.contrib import admin
from .models import Tip

# Register your models here.

admin.site.register(Tip)

# class TipForm(forms.ModelForm):

#     class Meta: 
#         model = Tip

#     def clean_hours_file(self):


