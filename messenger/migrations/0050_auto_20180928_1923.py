# Generated by Django 2.1 on 2018-09-28 14:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0049_auto_20180920_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 28, 19, 23, 46, 887544)),
        ),
    ]
