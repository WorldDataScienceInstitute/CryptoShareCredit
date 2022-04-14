# Generated by Django 3.2.5 on 2022-04-13 21:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0045_auto_20220410_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptocurrency',
            name='exchange_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 19, 21, 31, 9, 562650, tzinfo=utc), null=True),
        ),
    ]
