# Generated by Django 3.2.5 on 2023-04-04 00:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0130_auto_20230402_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 10, 0, 20, 51, 704809, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 4, 0, 20, 51, 706914, tzinfo=utc), null=True),
        ),
    ]
