# Generated by Django 3.2.5 on 2021-10-08 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20211008_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='DebitCardNumber',
        ),
        migrations.RemoveField(
            model_name='status',
            name='Pin',
        ),
    ]
