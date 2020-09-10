from django.db import models
from datetime import datetime

class Applications(models.Model):
    student = models.ForeignKey('Userinfo', models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey('Course', models.DO_NOTHING, blank=True, null=True)
    application_start_time = models.DateTimeField(blank=True, null=True)
    application_examine_time = models.DateTimeField(blank=True, null=True)
    application_result = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'applications'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    course_intro = models.TextField(blank=True, null=True)
    rule = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Post(models.Model):
    title = models.CharField(max_length=50)
    stared = models.IntegerField(blank=True, null=True)
    topped = models.IntegerField(blank=True, null=True)
    course = models.ForeignKey(Course, models.DO_NOTHING)
    owner = models.ForeignKey('Userinfo', models.DO_NOTHING)
    watches = models.IntegerField()
    tag = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post'


class UserCourse(models.Model):
    user = models.ForeignKey('Userinfo', models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(Course, models.DO_NOTHING, blank=True, null=True)
    watch_duration = models.TimeField(blank=True, null=True)
    watch_num = models.IntegerField(blank=True, null=True)
    user_identity = models.IntegerField(blank=True, null=True)
    activity = models.IntegerField(blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_course'


class UserPlayRecords(models.Model):
    user_video = models.ForeignKey('UserVideo', models.DO_NOTHING)
    played_time = models.TimeField(blank=True, null=True)
    start_play_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_play_records'


class UserVideo(models.Model):
    user = models.ForeignKey('Userinfo', models.DO_NOTHING, blank=True, null=True)
    video = models.ForeignKey('Videos', models.DO_NOTHING, blank=True, null=True)
    video_viewed_time = models.TimeField(blank=True, null=True)
    video_viewed_times = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_video'


class Userinfo(models.Model):
    username = models.CharField(unique=True, max_length=50)
    user_password = models.CharField(max_length=50)
    user_nickname = models.CharField(max_length=50, blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    phonenumber = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    qq = models.CharField(max_length=20, blank=True, null=True)
    teacher_identity = models.IntegerField(blank=True, null=True)
    school = models.CharField(max_length=50, blank=True, null=True)
    school_id = models.CharField(max_length=30, blank=True, null=True)
    realname = models.CharField(max_length=30, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userinfo'


class Videos(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    video_duration = models.TimeField(blank=True, null=True)
    local_address = models.CharField(max_length=50, blank=True, null=True)
    course = models.ForeignKey(Course, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'videos'