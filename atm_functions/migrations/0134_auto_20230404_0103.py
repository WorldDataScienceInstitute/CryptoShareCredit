# Generated by Django 3.2.5 on 2023-04-04 01:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0133_auto_20230404_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 10, 1, 3, 29, 882568, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 4, 1, 3, 29, 884732, tzinfo=utc), null=True),
        ),
    ]
