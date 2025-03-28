# Generated by Django 3.2.5 on 2022-01-08 22:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0029_rename_transactiontype_transactiona_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionb',
            name='creation_datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionb',
            name='end_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='transactionb',
            name='interest_rate',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='transactionb',
            name='start_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
