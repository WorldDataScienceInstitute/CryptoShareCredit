# Generated by Django 3.2.5 on 2021-10-29 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0014_remove_account_emailid'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='Phone',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
