# Generated by Django 3.2.5 on 2022-05-24 23:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('atm_functions', '0055_auto_20220522_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='state',
            field=models.CharField(max_length=57, null=True),
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='selfie_photo_url',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='blockchainwill',
            name='document_id_url',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='blockchainwill',
            name='selfie_photo_url',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='blockchainwill',
            name='video_url',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 30, 23, 4, 10, 583864, tzinfo=utc), null=True),
        ),
    ]
