# Generated by Django 3.2.5 on 2022-08-27 04:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0111_alter_address_expiration_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 2, 4, 15, 25, 110193, tzinfo=utc), null=True),
        ),
    ]
