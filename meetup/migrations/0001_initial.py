# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-05 12:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('start_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True, verbose_name='username')),
                ('organization', models.CharField(max_length=100, null=True)),
                ('image', models.ImageField(null=True, upload_to='profile')),
                ('biography', models.TextField(max_length=4000, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('brief', models.TextField(null=True, verbose_name='simple information')),
                ('description', models.TextField(null=True)),
                ('slide_url', models.URLField(null=True, verbose_name='A slide url')),
                ('pdf_url', models.URLField(null=True, verbose_name='A pdf url')),
                ('video_url', models.URLField(null=True, verbose_name='A video url')),
                ('is_recordable', models.BooleanField(default=True, verbose_name='recordable condition')),
                ('is_main_event', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProgramCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=255, null=True)),
                ('description', models.TextField(null=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.AddField(
            model_name='program',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='meetup.ProgramCategory', verbose_name='The category which this program is belonged'),
        ),
        migrations.AddField(
            model_name='program',
            name='meet_up',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='meetup.MeetUp'),
        ),
        migrations.AddField(
            model_name='program',
            name='speakers',
            field=models.ManyToManyField(to='meetup.Speaker'),
        ),
        migrations.AddField(
            model_name='meetup',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetup.Venue'),
        ),
    ]
