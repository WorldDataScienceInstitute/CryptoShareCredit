# Generated by Django 3.2.5 on 2022-01-23 07:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0038_alter_address_expiration_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 30, 1, 0, 49, 87341), null=True),
        ),
    ]
