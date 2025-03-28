# Generated by Django 3.2.5 on 2022-10-26 00:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0126_auto_20220907_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='card_pin',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 1, 0, 49, 54, 307463, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 26, 0, 49, 54, 308463, tzinfo=utc), null=True),
        ),
    ]
