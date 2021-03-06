# Generated by Django 2.0.4 on 2018-05-19 19:42

import django.core.validators
from django.db import migrations, models
import tips.models


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0014_remove_employee_total_hours'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tip',
            old_name='wee_friday_cash_tips',
            new_name='wee_Friday_cash_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_friday_cash_tips_currency',
            new_name='wee_Friday_cash_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_friday_cred_tips',
            new_name='wee_Friday_cred_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_friday_cred_tips_currency',
            new_name='wee_Friday_cred_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_monday_cash_tips',
            new_name='wee_Monday_cash_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_monday_cash_tips_currency',
            new_name='wee_Monday_cash_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_monday_cred_tips',
            new_name='wee_Monday_cred_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_monday_cred_tips_currency',
            new_name='wee_Monday_cred_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_saturday_cash_tips',
            new_name='wee_Saturday_cash_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_saturday_cash_tips_currency',
            new_name='wee_Saturday_cash_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_saturday_cred_tips',
            new_name='wee_Saturday_cred_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_saturday_cred_tips_currency',
            new_name='wee_Saturday_cred_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_sunday_cash_tips',
            new_name='wee_Sunday_cash_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_sunday_cash_tips_currency',
            new_name='wee_Sunday_cash_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_sunday_cred_tips',
            new_name='wee_Sunday_cred_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_sunday_cred_tips_currency',
            new_name='wee_Sunday_cred_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_thursday_cash_tips',
            new_name='wee_Thursday_cash_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_thursday_cash_tips_currency',
            new_name='wee_Thursday_cash_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_thursday_cred_tips',
            new_name='wee_Thursday_cred_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_thursday_cred_tips_currency',
            new_name='wee_Thursday_cred_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_tuesday_cash_tips',
            new_name='wee_Tuesday_cash_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_tuesday_cash_tips_currency',
            new_name='wee_Tuesday_cash_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_tuesday_cred_tips',
            new_name='wee_Tuesday_cred_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_tuesday_cred_tips_currency',
            new_name='wee_Tuesday_cred_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_wednesday_cash_tips',
            new_name='wee_Wednesday_cash_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_wednesday_cash_tips_currency',
            new_name='wee_Wednesday_cash_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_wednesday_cred_tips',
            new_name='wee_Wednesday_cred_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='wee_wednesday_cred_tips_currency',
            new_name='wee_Wednesday_cred_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_friday_cash_tips',
            new_name='west7_Friday_cash_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_friday_cash_tips_currency',
            new_name='west7_Friday_cash_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_friday_cred_tips',
            new_name='west7_Friday_cred_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_friday_cred_tips_currency',
            new_name='west7_Friday_cred_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_monday_cash_tips',
            new_name='west7_Monday_cash_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_monday_cash_tips_currency',
            new_name='west7_Monday_cash_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_monday_cred_tips',
            new_name='west7_Monday_cred_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_monday_cred_tips_currency',
            new_name='west7_Monday_cred_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_saturday_cash_tips',
            new_name='west7_Saturday_cash_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_saturday_cash_tips_currency',
            new_name='west7_Saturday_cash_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_saturday_cred_tips',
            new_name='west7_Saturday_cred_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_saturday_cred_tips_currency',
            new_name='west7_Saturday_cred_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_sunday_cash_tips',
            new_name='west7_Sunday_cash_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_sunday_cash_tips_currency',
            new_name='west7_Sunday_cash_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_sunday_cred_tips',
            new_name='west7_Sunday_cred_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_sunday_cred_tips_currency',
            new_name='west7_Sunday_cred_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_thursday_cash_tips',
            new_name='west7_Thursday_cash_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_thursday_cash_tips_currency',
            new_name='west7_Thursday_cash_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_thursday_cred_tips',
            new_name='west7_Thursday_cred_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_thursday_cred_tips_currency',
            new_name='west7_Thursday_cred_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_tuesday_cash_tips',
            new_name='west7_Tuesday_cash_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_tuesday_cash_tips_currency',
            new_name='west7_Tuesday_cash_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_tuesday_cred_tips',
            new_name='west7_Tuesday_cred_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_tuesday_cred_tips_currency',
            new_name='west7_Tuesday_cred_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_wednesday_cash_tips',
            new_name='west7_Wednesday_cash_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_wednesday_cash_tips_currency',
            new_name='west7_Wednesday_cash_tips_currency',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_wednesday_cred_tips',
            new_name='west7_Wednesday_cred_tips',
        ),
        migrations.RenameField(
            model_name='tip',
            old_name='west7_wednesday_cred_tips_currency',
            new_name='west7_Wednesday_cred_tips_currency',
        ),
        migrations.RemoveField(
            model_name='tip',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='tip',
            name='hours_file',
            field=models.FileField(upload_to=tips.models.getUploadFileName, validators=[django.core.validators.FileExtensionValidator(['csv'])]),
        ),
        migrations.AlterField(
            model_name='tip',
            name='title',
            field=models.DateField(),
        ),
    ]
