# Generated by Django 3.2.5 on 2022-08-06 04:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0079_auto_20220805_2310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='id_business',
        ),
        migrations.AddField(
            model_name='business',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddField(
            model_name='business',
            name='system_name',
            field=models.CharField(default='cryptoshare banq', max_length=57),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 12, 4, 16, 47, 543275, tzinfo=utc), null=True),
        ),
    ]
