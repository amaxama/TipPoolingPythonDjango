# Generated by Django 2.0.4 on 2018-05-07 18:55

from django.db import migrations


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('tips', '0008_auto_20180507_1854'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tip',
            old_name='hours_File',
            new_name='hours_file',
        ),
    ]
