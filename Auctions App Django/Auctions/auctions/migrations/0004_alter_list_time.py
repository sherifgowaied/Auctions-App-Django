# Generated by Django 4.0.2 on 2022-03-07 01:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_list_time_alter_list_watched_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 7, 1, 42, 52, 305327, tzinfo=utc)),
        ),
    ]