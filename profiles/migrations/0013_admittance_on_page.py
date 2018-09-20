# Generated by Django 2.1 on 2018-09-09 17:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0012_auto_20180909_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='admittance',
            name='on_page',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='profile_admittance', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
