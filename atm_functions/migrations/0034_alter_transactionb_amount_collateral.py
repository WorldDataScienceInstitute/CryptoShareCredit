# Generated by Django 3.2.5 on 2022-01-09 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0033_rename_amount_colateral_transactionb_amount_collateral'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionb',
            name='amount_collateral',
            field=models.DecimalField(decimal_places=8, max_digits=15, null=True),
        ),
    ]
