# Generated by Django 4.2.5 on 2023-10-06 03:04

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('vetapp', '0016_alter_appointment_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='phone',
            field=phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31),
        ),
    ]