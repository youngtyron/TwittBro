# Generated by Django 2.1 on 2018-09-04 14:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0014_auto_20180903_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 4, 19, 31, 59, 177549)),
        ),
    ]
