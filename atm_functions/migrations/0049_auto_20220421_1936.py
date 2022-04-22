# Generated by Django 3.2.5 on 2022-04-22 00:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0048_auto_20220413_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='birthdate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='country',
            field=models.CharField(max_length=57, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 28, 0, 36, 25, 929207, tzinfo=utc), null=True),
        ),
    ]
