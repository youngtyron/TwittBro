# Generated by Django 2.1 on 2018-09-04 15:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0023_auto_20180904_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 4, 20, 47, 21, 468163)),
        ),
    ]
