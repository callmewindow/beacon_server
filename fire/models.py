from django.db import models
from datetime import datetime
#课程圈子
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_intro = models.TextField(blank=True, null=True)
    rule = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    is_open = models.IntegerField(default=0)
    teacher_id = models.ForeignKey('Userinfo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'course'

#楼层
class Floor(models.Model):
    author = models.ForeignKey('Userinfo', on_delete=models.SET_DEFAULT, default=1)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
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
    stared = models.IntegerField(blank=True, default=0)
    topped = models.IntegerField(blank=True, default=0)
    course = models.ForeignKey(Course, models.DO_NOTHING)
    owner = models.ForeignKey('Userinfo', on_delete=models.CASCADE)
    watches = models.IntegerField(default=0)
    tag = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'post'

#用户-课程记录
class UserCourse(models.Model):
    user = models.ForeignKey('Userinfo', on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    watch_duration = models.IntegerField(blank=True, null=True)
    watch_num = models.IntegerField(blank=True, null=True)
    user_identity = models.IntegerField(blank=True, default=0)
    activity = models.IntegerField(blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'user_course'

#用户-播放记录
class UserPlayRecords(models.Model):
    user_video = models.ForeignKey('UserVideo', on_delete=models.CASCADE)
    played_time = models.IntegerField(blank=True, null=True)
    start_play_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'user_play_records'

#用户-视频记录
class UserVideo(models.Model):
    user = models.ForeignKey('Userinfo', on_delete=models.CASCADE, blank=True, null=True)
    video = models.ForeignKey('Videos', on_delete=models.CASCADE, blank=True, null=True)
    video_viewed_time = models.IntegerField(blank=True, null=True)
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
    video_duration = models.IntegerField(blank=True, null=True)
    local_address = models.CharField(max_length=100, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    upload_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'videos'

#点赞记录
class LikeRecord(models.Model):
    student = models.ForeignKey('Userinfo', on_delete=models.CASCADE, blank=True, null=True)
    floor = models.ForeignKey('Floor', on_delete=models.CASCADE, blank=True, null=True)
    like_type = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'like_record'

#课程申请记录
class CourseApplication(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('Userinfo', on_delete=models.CASCADE, blank=True, null=True)
    result = models.IntegerField(blank=True, default=0)
    application_time = models.DateTimeField(blank=True, null=True)
    content = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'course_application'

#好友申请记录
class FriendApplication(models.Model):
    applicant = models.ForeignKey('Userinfo', on_delete=models.CASCADE, blank=True, null=True, related_name='applicant')
    target = models.ForeignKey('Userinfo', on_delete=models.CASCADE, blank=True, null=True, related_name='target')
    application_content = models.CharField(max_length=200, blank=True, null=True)
    application_time = models.DateTimeField(blank=True, null=True)
    result = models.IntegerField(blank=True, default=0)
    handle_content = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'friend_application'

#好友记录
class FriendRecord(models.Model):
    user1 = models.ForeignKey('Userinfo', on_delete=models.CASCADE, blank=True, null=True, related_name='user1')
    user2 = models.ForeignKey('Userinfo', on_delete=models.CASCADE, blank=True, null=True, related_name='user2')

    class Meta:
        db_table = 'friend_record'

#系统消息
class SystemMessage(models.Model):
    target = models.ForeignKey('Userinfo', on_delete=models.CASCADE, blank=True, null=True)
    message_title = models.CharField(max_length=200, blank=True, null=True)
    message_content = models.CharField(max_length=200, blank=True, null=True)
    is_read = models.IntegerField(blank=True, default=0)
    send_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'system_message'

#私信
class PrivateMessage(models.Model):
    sender = models.ForeignKey('Userinfo', on_delete=models.CASCADE, blank=True, null=True, related_name='sender')
    receiver = models.ForeignKey('Userinfo', on_delete=models.CASCADE, blank=True, null=True, related_name='receiver')
    content = models.CharField(max_length=200, blank=True, null=True)
    send_time = models.DateTimeField(blank=True, null=True)
    is_read = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'private_message'