from django.shortcuts import render
from fire.models import *
from django.http.response import HttpResponse
import datetime
import os
from moviepy.editor import VideoFileClip

def createCourse(request):
    if(request.method != 'POST'):
        msg = 'fail'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    dict=request.POST
    course_name=dict.get('course_name')
    course_intro=dict.get('course_intro')
    rule=dict.get('rule')
    start_time=dict.get('start_time')
    end_time=dict.get('end_time')
    profession=dict.get('profession')

    if course_name is None or course_intro is None or rule is None or start_time is None or end_time is None or profession is None:
        msg = 'empty input'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    try:
        result = Course.objects.filter(course_name=course_name)
    except Exception:
        msg = 'database search course_name in Course error'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    if result:
        msg = 'course_name exit'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    course=Course()
    course.course_name=course_name
    course.course_intro=course_intro
    course.rule=rule
    course.start_time=datetime.datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')
    course.end_time=datetime.datetime.strftime(end_time, '%Y-%m-%d %H:%M:%S')
    course.profession=profession
    try:
        course.save()
    except Exception:
        msg = 'database save course error'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    courseInDatabase=Course.objects.filter(course_name=course_name)
    id=courseInDatabase.id
    res = "{\"msg\": \"success\", \"id\": " + str(id) + "}"
    return HttpResponse(res)



def uploadVideo(request):
    if (request.method != 'POST'):
        msg = 'fail'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    dict = request.POST
    title = dict.get('title')
    introduction = dict.get('introduction')
    # video_duration = dict.get('video_duration')
    course_name = dict.get('course_name')
    upload_time = dict.get('upload_time')
    video_file = request.FILES.get('video')

    if title is None or introduction is None or course_name is None or upload_time is None or video_file is None:
        msg = 'empty input'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    try:
        result = Videos.objects.filter(title = title)
    except Exception:
        msg = 'database search video in Vedios error'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    if result:
        msg = 'video title exit'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    video = Videos()
    video.title = title
    video.introduction = introduction
    video.upload_time = datetime.datetime.strftime(upload_time, '%Y-%m-%d %H:%M:%S')

    try:
        course = Course.objects.filter(course_name = course_name)
    except Exception:
        msg = 'database search course_name in Course error'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    if not course:
        msg = 'course do not exit'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    video.course = course

    video_name = title + '.mp4'
    video_path = os.path.join('/fire/media', video_name)
    f = open(video_path, 'wb')
    for i in video_file.chunks():
        f.write(i)
    f.close()
    video.local_address = '/fire/media/' + video_name

    clip = VideoFileClip('/fire/media/' + video_name)
    video.video_duration = clip

    try:
        video.save()
    except Exception:
        msg = 'database save video error'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    msg = 'success'
    res = "{\"msg\": \"" + msg + "\"}"
    return HttpResponse(res)



# 每行依次是，学校，学号，真实姓名，邮箱
def uploadCourseUser(request):
    if (request.method != 'POST'):
        msg = 'fail'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    csv_file = request.FILES.get('csv_file')
    course_name = request.POST.get('course_name')
    course_id = request.POST.get('course_id')

    if csv_file is None or course_name is None or course_id is None:
        msg = 'empty input'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    if not csv_file.name.endswith('.csv'):
        msg = 'file is not csv type'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    file_data = csv_file.read().decode('utf-8')
    lines = file_data.spilt('\n')
    for line in lines:
        fields = line.spilt(',')
        realname = fields[2]

        try:
            user = Userinfo.objects.filter(realname = realname)
        except Exception:
            msg = 'database search realname in UserInfo error'
            res = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(res)
        if not user:
            userInfo = Userinfo()
            userInfo.school = fields[0]
            userInfo.school_id = fields[1]
            userInfo.realname = fields[2]
            userInfo.email = fields[3]
            try:
                Userinfo.save()
            except Exception:
                msg = 'database save userInfo error'
                res = "{\"msg\": \"" + msg + "\"}"
                return HttpResponse(res)
        try:
            user = UserCourse.objects.filter(realname = realname)
        except Exception:
            msg = 'database search realname in UserCourse error'
            res = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(res)
        if not user:
            userCourse = UserCourse()
            try:
                user = Userinfo.objects.filter(realname=realname)
            except Exception:
                msg = 'database search realname in UserInfo error'
                res = "{\"msg\": \"" + msg + "\"}"
                return HttpResponse(res)
            userCourse.user = user
            try:
                course = Course.objects.filter(id=course_id)
            except Exception:
                msg = 'database search id in Course error'
                res = "{\"msg\": \"" + msg + "\"}"
                return HttpResponse(res)
            userCourse.course = course
            userCourse.user_identity = 1
            try:
                userCourse.save()
            except Exception:
                msg = 'database save userCourse error'
                res = "{\"msg\": \"" + msg + "\"}"
                return HttpResponse(res)

    msg = 'success'
    res = "{\"msg\": \"" + msg + "\"}"
    return HttpResponse(res)



url_zzc = [
    url('createCourse', createCourse),
    url('uploadVideo', uploadVideo),
]