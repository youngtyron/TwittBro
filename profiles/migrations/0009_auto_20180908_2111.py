# Generated by Django 2.1 on 2018-09-08 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20180908_2110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='type',
        ),
        migrations.AddField(
            model_name='profile',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]
