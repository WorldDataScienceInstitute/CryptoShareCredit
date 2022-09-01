# Generated by Django 3.2.5 on 2022-09-01 03:49

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('atm_functions', '0114_auto_20220830_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 7, 3, 49, 7, 717228, tzinfo=utc), null=True),
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id_insurance', models.AutoField(primary_key=True, serialize=False)),
                ('plan', models.CharField(max_length=10)),
                ('amount', models.DecimalField(decimal_places=8, max_digits=18)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
