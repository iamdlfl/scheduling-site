# Generated by Django 3.1.2 on 2021-02-07 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='shifts',
            field=models.IntegerField(default=0),
        ),
    ]
