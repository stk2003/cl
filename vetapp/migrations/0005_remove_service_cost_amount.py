# Generated by Django 4.2.5 on 2023-10-03 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vetapp', '0004_cost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='cost_amount',
        ),
    ]
