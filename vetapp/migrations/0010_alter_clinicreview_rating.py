# Generated by Django 4.2.5 on 2023-10-04 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vetapp', '0009_alter_clinic_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicreview',
            name='rating',
            field=models.DecimalField(decimal_places=0, max_digits=3),
        ),
    ]