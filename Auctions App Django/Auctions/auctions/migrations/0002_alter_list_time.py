# Generated by Django 4.0.2 on 2022-03-06 07:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 6, 7, 4, 52, 574745, tzinfo=utc)),
        ),
    ]
