# Generated by Django 2.0.4 on 2018-05-07 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('tips', '0007_auto_20180502_0603'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tips',
            new_name='Tip',
        ),
        migrations.RemoveField(
            model_name='location',
            name='tip_id',
        ),
        migrations.AddField(
            model_name='location',
            name='tips',
            field=models.ManyToManyField(to='tips.Tip'),
        ),
    ]
