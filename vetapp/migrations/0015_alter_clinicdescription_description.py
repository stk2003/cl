# Generated by Django 4.2.5 on 2023-10-04 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vetapp', '0014_delete_singletonclinicdescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicdescription',
            name='description',
            field=models.TextField(unique=True),
        ),
    ]