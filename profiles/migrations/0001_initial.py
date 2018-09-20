# Generated by Django 2.1 on 2018-08-26 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('messenger', '0002_auto_20180826_1931'),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('time', models.DateTimeField()),
                ('status', models.CharField(choices=[('Not read', 'Not read'), ('Read', 'Read')], default='Not read', max_length=30)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('about', models.CharField(choices=[('Like', 'Like'), ('Repost', 'Repost'), ('Subscribe', 'Subscribe'), ('Another', 'Another')], default='Another', max_length=30)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('sex', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Not specified', 'Not specified')], max_length=100, null=True)),
                ('summary', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('registrated', models.DateField()),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('avatar', models.ImageField(upload_to='images/')),
                ('dialogues', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='messenger.Chat')),
            ],
        ),
        migrations.CreateModel(
            name='Subscrib',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subs_date', models.DateTimeField()),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('who', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcribed', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='notificator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notices', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
