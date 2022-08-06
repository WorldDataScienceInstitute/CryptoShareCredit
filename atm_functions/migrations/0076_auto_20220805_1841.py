# Generated by Django 3.2.5 on 2022-08-05 23:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0075_auto_20220805_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripetransaction',
            name='transaction_type_internal',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 11, 23, 40, 59, 933728, tzinfo=utc), null=True),
        ),
    ]
