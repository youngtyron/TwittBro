# Generated by Django 2.1 on 2018-09-06 14:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0031_auto_20180906_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 6, 19, 38, 32, 435004)),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
