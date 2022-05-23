# Generated by Django 3.2.5 on 2022-05-23 01:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('atm_functions', '0053_auto_20220508_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 29, 1, 21, 8, 439967, tzinfo=utc), null=True),
        ),
        migrations.CreateModel(
            name='BlockchainWill',
            fields=[
                ('id_w', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=15)),
                ('full_legal_name', models.CharField(max_length=255, null=True)),
                ('birthdate', models.DateField(null=True)),
                ('birth_country', models.CharField(max_length=57, null=True)),
                ('associated_email1', models.CharField(max_length=40, null=True)),
                ('associated_email2', models.CharField(max_length=40, null=True)),
                ('associated_email3', models.CharField(max_length=40, null=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Beneficiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_legal_name', models.CharField(max_length=255)),
                ('birthdate', models.DateField()),
                ('birth_country', models.CharField(max_length=57)),
                ('relationship', models.CharField(max_length=50)),
                ('associated_email1', models.CharField(max_length=40, null=True)),
                ('associated_email2', models.CharField(max_length=40, null=True)),
                ('will_percentage', models.IntegerField()),
                ('blockchain_wills', models.ManyToManyField(to='atm_functions.BlockchainWill')),
            ],
        ),
    ]
