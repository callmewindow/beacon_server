# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-09-10 10:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_start_time', models.DateTimeField(blank=True, null=True)),
                ('application_examine_time', models.DateTimeField(blank=True, null=True)),
                ('application_result', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'applications',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=100)),
                ('course_intro', models.TextField(blank=True, null=True)),
                ('rule', models.TextField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('profession', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'course',
            },
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('post_time', models.DateTimeField(blank=True, null=True)),
                ('floor_num', models.IntegerField()),
                ('reply_floor', models.IntegerField()),
                ('like_num', models.IntegerField()),
            ],
            options={
                'db_table': 'floor',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('stared', models.IntegerField(blank=True, null=True)),
                ('topped', models.IntegerField(blank=True, null=True)),
                ('watches', models.IntegerField()),
                ('tag', models.CharField(blank=True, max_length=100, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fire.Course')),
            ],
            options={
                'db_table': 'post',
            },
        ),
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watch_duration', models.TimeField(blank=True, null=True)),
                ('watch_num', models.IntegerField(blank=True, null=True)),
                ('user_identity', models.IntegerField(blank=True, null=True)),
                ('activity', models.IntegerField(blank=True, null=True)),
                ('point', models.IntegerField(blank=True, null=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fire.Course')),
            ],
            options={
                'db_table': 'user_course',
            },
        ),
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('user_password', models.CharField(max_length=100)),
                ('user_nickname', models.CharField(blank=True, max_length=100, null=True)),
                ('introduction', models.TextField(blank=True, null=True)),
                ('phonenumber', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('qq', models.CharField(blank=True, max_length=100, null=True)),
                ('teacher_identity', models.IntegerField(blank=True, null=True)),
                ('school', models.CharField(blank=True, max_length=100, null=True)),
                ('school_id', models.CharField(blank=True, max_length=100, null=True)),
                ('realname', models.CharField(blank=True, max_length=100, null=True)),
                ('profession', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'userinfo',
            },
        ),
        migrations.CreateModel(
            name='UserPlayRecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('played_time', models.TimeField(blank=True, null=True)),
                ('start_play_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_play_records',
            },
        ),
        migrations.CreateModel(
            name='UserVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_viewed_time', models.TimeField(blank=True, null=True)),
                ('video_viewed_times', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fire.Userinfo')),
            ],
            options={
                'db_table': 'user_video',
            },
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('introduction', models.TextField(blank=True, null=True)),
                ('video_duration', models.TimeField(blank=True, null=True)),
                ('local_address', models.CharField(blank=True, max_length=100, null=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fire.Course')),
            ],
            options={
                'db_table': 'videos',
            },
        ),
        migrations.AddField(
            model_name='uservideo',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fire.Videos'),
        ),
        migrations.AddField(
            model_name='userplayrecords',
            name='user_video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fire.UserVideo'),
        ),
        migrations.AddField(
            model_name='usercourse',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fire.Userinfo'),
        ),
        migrations.AddField(
            model_name='post',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fire.Userinfo'),
        ),
        migrations.AddField(
            model_name='floor',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fire.Userinfo'),
        ),
        migrations.AddField(
            model_name='floor',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fire.Post'),
        ),
        migrations.AddField(
            model_name='applications',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fire.Course'),
        ),
        migrations.AddField(
            model_name='applications',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fire.Userinfo'),
        ),
    ]