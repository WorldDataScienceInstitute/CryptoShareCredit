# Generated by Django 3.2.5 on 2022-08-08 00:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0083_auto_20220805_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 14, 0, 17, 26, 978209, tzinfo=utc), null=True),
        ),
        migrations.DeleteModel(
            name='TransactionC',
        ),
    ]
