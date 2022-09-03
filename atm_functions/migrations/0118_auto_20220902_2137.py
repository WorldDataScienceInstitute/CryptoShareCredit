# Generated by Django 3.2.5 on 2022-09-03 02:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0117_auto_20220901_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurance',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 3, 2, 37, 29, 561900, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 9, 2, 37, 29, 561040, tzinfo=utc), null=True),
        ),
    ]
