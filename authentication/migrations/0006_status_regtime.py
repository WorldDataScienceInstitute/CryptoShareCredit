# Generated by Django 3.2.5 on 2021-10-08 19:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20211008_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='regtime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
