# Generated by Django 2.1 on 2018-08-27 15:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0006_auto_20180827_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 27, 20, 42, 37, 449040)),
        ),
    ]
