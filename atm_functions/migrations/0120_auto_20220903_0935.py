# Generated by Django 3.2.5 on 2022-09-03 14:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0119_auto_20220902_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 9, 14, 35, 4, 44864, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 3, 14, 35, 4, 45870, tzinfo=utc), null=True),
        ),
    ]
