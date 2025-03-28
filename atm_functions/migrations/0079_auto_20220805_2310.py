# Generated by Django 3.2.5 on 2022-08-06 04:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0078_auto_20220805_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='creation_datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 12, 4, 10, 46, 843246, tzinfo=utc), null=True),
        ),
    ]
