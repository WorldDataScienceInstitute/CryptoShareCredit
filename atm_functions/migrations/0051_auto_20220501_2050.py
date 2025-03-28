# Generated by Django 3.2.5 on 2022-05-02 01:50

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0050_auto_20220428_1740'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionc',
            old_name='crypto_id_swap_to',
            new_name='crypto_id_to',
        ),
        migrations.RemoveField(
            model_name='transactionc',
            name='network_fee',
        ),
        migrations.AddField(
            model_name='transactionc',
            name='address_destination_ed',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='transactionc',
            name='address_refund_ed',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='transactionc',
            name='creation_datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 8, 1, 50, 3, 116182, tzinfo=utc), null=True),
        ),
    ]
