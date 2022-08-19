# Generated by Django 3.2.5 on 2022-08-18 02:23

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('atm_functions', '0096_auto_20220817_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 24, 2, 23, 56, 63087, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='creditstransaction',
            name='receiver_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_receiver_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='creditstransaction',
            name='sender_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_sender_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
