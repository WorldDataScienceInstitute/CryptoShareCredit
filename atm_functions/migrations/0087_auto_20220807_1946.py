# Generated by Django 3.2.5 on 2022-08-08 00:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('atm_functions', '0086_auto_20220807_1923'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionc',
            old_name='currency_name',
            new_name='digital_currency_name',
        ),
        migrations.RemoveField(
            model_name='transactionc',
            name='user',
        ),
        migrations.AddField(
            model_name='transactionc',
            name='receiver_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_user', to='auth.user'),
        ),
        migrations.AddField(
            model_name='transactionc',
            name='sender_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_user', to='auth.user'),
        ),
    ]
