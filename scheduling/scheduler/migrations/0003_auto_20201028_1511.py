# Generated by Django 3.1.2 on 2020-10-28 20:11

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_auto_20201013_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleschema',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scheduleschema',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 28, 20, 11, 10, 160083, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
