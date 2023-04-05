# Generated by Django 3.2.5 on 2023-04-04 00:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0132_auto_20230404_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 10, 0, 32, 18, 97640, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 4, 0, 32, 18, 99740, tzinfo=utc), null=True),
        ),
    ]
