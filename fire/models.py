from django.db import models
from datetime import datetime
#申请
class Applications(models.Model):
    student = models.ForeignKey('Userinfo', models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey('Course', models.DO_NOTHING, blank=True, null=True)
    application_start_time = models.DateTimeField(blank=True, null=True)
    application_examine_time = models.DateTimeField(blank=True, null=True)
    application_result = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'applications'
#课程圈子
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_intro = models.TextField(blank=True, null=True)
    rule = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    is_open = models.IntegerField(default=0)

    class Meta:
        db_table = 'course'

#楼层
class Floor(models.Model):
    author = models.ForeignKey('Userinfo', models.DO_NOTHING)
    post = models.ForeignKey('Post', models.DO_NOTHING)
    content = models.TextField(blank=True, null=True)
    post_time = models.DateTimeField(blank=True, null=True)
    floor_num = models.IntegerField()
    reply_floor = models.IntegerField()
    like_num = models.IntegerField()

    class Meta:
        db_table = 'floor'

#帖子
class Post(models.Model):
    title = models.CharField(max_length=100)
    stared = models.IntegerField(blank=True, null=True)
    topped = models.IntegerField(blank=True, null=True)
    course = models.ForeignKey(Course, models.DO_NOTHING)
    owner = models.ForeignKey('Userinfo', models.DO_NOTHING)
    watches = models.IntegerField()
    tag = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'post'

#用户-课程记录
class UserCourse(models.Model):
    user = models.ForeignKey('Userinfo', models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(Course, models.DO_NOTHING, blank=True, null=True)
    watch_duration = models.TimeField(blank=True, null=True)
    watch_num = models.IntegerField(blank=True, null=True)
    user_identity = models.IntegerField(blank=True, null=True)
    activity = models.IntegerField(blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'user_course'

#用户-播放记录
class UserPlayRecords(models.Model):
    user_video = models.ForeignKey('UserVideo', models.DO_NOTHING)
    played_time = models.TimeField(blank=True, null=True)
    start_play_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'user_play_records'

#用户-视频记录
class UserVideo(models.Model):
    user = models.ForeignKey('Userinfo', models.DO_NOTHING, blank=True, null=True)
    video = models.ForeignKey('Videos', models.DO_NOTHING, blank=True, null=True)
    video_viewed_time = models.TimeField(blank=True, null=True)
    video_viewed_times = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'user_video'

#用户
class Userinfo(models.Model):
    username = models.CharField(unique=True, max_length=100)
    user_password = models.CharField(max_length=100)
    user_nickname = models.CharField(max_length=100, blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    phonenumber = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    qq = models.CharField(max_length=100, blank=True, null=True)
    teacher_identity = models.IntegerField(blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    school_id = models.CharField(max_length=100, blank=True, null=True)
    realname = models.CharField(max_length=100, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'userinfo'

#视频
class Videos(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    video_duration = models.TimeField(blank=True, null=True)
    local_address = models.CharField(max_length=100, blank=True, null=True)
    course = models.ForeignKey(Course, models.DO_NOTHING, blank=True, null=True)
    upload_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'videos'

#点赞记录
class LikeRecord(models.Model):
    student = models.ForeignKey('Userinfo', models.DO_NOTHING, blank=True, null=True)
    floor = models.ForeignKey('Floor', models.DO_NOTHING, blank=True, null=True)
    like_type = models.IntegerField(blank=True, null=True)