# Generated by Django 3.1.1 on 2021-01-28 12:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quick_note', '0002_auto_20210122_0226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usernotes',
            name='shared_visits',
        ),
        migrations.AlterField(
            model_name='usernotes',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2021, 1, 28, 12, 50, 7, 186781, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='usernotes',
            name='last_edit',
            field=models.DateField(default=datetime.datetime(2021, 1, 28, 12, 50, 7, 186781, tzinfo=utc), verbose_name='Last Edited date'),
        ),
    ]
