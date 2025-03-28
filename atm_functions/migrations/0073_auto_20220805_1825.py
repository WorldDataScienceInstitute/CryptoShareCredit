# Generated by Django 3.2.5 on 2022-08-05 23:25

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0072_auto_20220805_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripetransactions',
            name='creation_datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 11, 23, 25, 6, 527206, tzinfo=utc), null=True),
        ),
    ]
