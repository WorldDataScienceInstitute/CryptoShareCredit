# Generated by Django 3.2.5 on 2022-08-14 23:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0094_auto_20220814_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 20, 23, 54, 33, 150423, tzinfo=utc), null=True),
        ),
    ]
