# Generated by Django 3.2.5 on 2022-09-03 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0005_purchasehistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasehistory',
            name='paid_price',
            field=models.DecimalField(decimal_places=8, max_digits=18),
        ),
    ]
