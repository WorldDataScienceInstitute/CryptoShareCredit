# Generated by Django 3.2.5 on 2022-08-27 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='system_category',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
