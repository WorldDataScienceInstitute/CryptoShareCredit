# Generated by Django 3.2.5 on 2022-01-08 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0030_auto_20220108_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionb',
            name='amount_colateral',
            field=models.DecimalField(decimal_places=8, max_digits=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionb',
            name='currency_name_collateral',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='currency_name_collateral', to='atm_functions.cryptocurrency'),
            preserve_default=False,
        ),
    ]
