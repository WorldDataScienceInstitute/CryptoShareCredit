# Generated by Django 3.2.5 on 2023-04-02 08:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0129_auto_20230402_0128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 8, 8, 5, 20, 85647, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 2, 8, 5, 20, 89625, tzinfo=utc), null=True),
        ),
    ]
