# Generated by Django 4.2.5 on 2023-10-06 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vetapp', '0019_appointment_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='phone',
        ),
    ]
