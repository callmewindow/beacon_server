import json
from builtins import type, eval

from django.shortcuts import render
from fire.models import *
from django.http.response import HttpResponse
import datetime
import os
from moviepy.editor import VideoFileClip
from django.conf.urls import url


def createCourse(request):
    if(request.method != 'POST'):
        msg = 'fail'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    # print(request.POST)
    # temp4 = eval(str(request.body)[1:])
    # dict = json.loads(temp4)['courseEntity']
    # course_name = dict['course_name']
    # course_intro = dict['course_intro']
    # start_time = dict['start_time']
    # end_time = dict['end_time']
    # profession = dict['profession']

    # msg = str(type(request.POST))
    # res = "{\"msg\": \"" + request.POST + "\"}"
    # return HttpResponse(res)
    # dict=request.POST.get('courseEntity')
    # res = "{\"msg\": \"" + str(type(dict)) + "\"}"
    # return HttpResponse(res)
    dict = request.POST
    print(dict)
    course_name=dict.get('course_name')
    course_intro=dict.get('course_intro')
    # rule=dict.get('rule')
    start_time=dict.get('start_time')
    end_time=dict.get('end_time')
    profession=dict.get('profession')

    # if course_name is None or course_intro is None or start_time is None or end_time is None or profession is None:
    #     msg = 'empty input'
    #     res = "{\"msg\": \"" + msg + "\"}"
    #     return HttpResponse(res)

    # try:
    #     result = Course.objects.filter(course_name=course_name)
    # except Exception:
    #     msg = 'database search course_name in Course error'
    #     res = "{\"msg\": \"" + msg + "\"}"
    #     return HttpResponse(res)
    # if result:
    #     msg = 'course_name exit'
    #     res = "{\"msg\": \"" + msg + "\"}"
    #     return HttpResponse(res)

    course=Course()
    course.course_name=course_name
    course.course_intro=course_intro
    # course.rule=rule
    course.start_time=datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    course.end_time=datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    course.profession=profession




    try:
        course.save()
    except Exception:
        msg = 'database save course error'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)


    # courseInDatabase=Course.objects.filter(course_name=course_name)
    # id=courseInDatabase.id
    # res = "{\"msg\": \"success\", \"id\": " + str(id) + "}"
    # return HttpResponse(res)

    msg = 'success'
    # res = "{\"msg\": \"" + course_name + " " + course_intro + " " + start_time + " " + end_time + " " + profession + "\"}"
    res = "{\"msg\": \"" + msg + "\"}"
    return HttpResponse(res)



# def uploadVideo(request):
#     if (request.method != 'POST'):
#         msg = 'fail'
#         res = "{\"msg\": \"" + msg + "\"}"
#         return HttpResponse(res)
#
#     # video_file = request.FILES.get('video')
#     # if video_file:
#     #     msg = 'success'
#     #     res = "{\"msg\": \"" + msg + "\"}"
#     #     return HttpResponse(res)
#     # else:
#     #     msg = 'fail'
#     #     res = "{\"msg\": \"" + msg + "\"}"
#     #     return HttpResponse(res)
#
#
#     # temp4 = eval(str(request.body)[1:])
#     # dict = json.loads(temp4)['videoEntity']
#     # title = dict['title']
#     # introduction = dict['introduction']
#     # course_id = dict['course_id']
#     # upload_time = dict['upload_time']
#     # video_file = request.FILES.get('video')
#
#     dict = request.POST
#     title = dict.get('title')
#     introduction = dict.get('introduction')
#     # video_duration = dict.get('video_duration')
#     # course_name = dict.get('course_name')
#     course_id = dict.get('course_id')
#     upload_time = dict.get('upload_time')
#     video_file = request.FILES.get('file')
#     print(title)
#     print(introduction)
#     print(course_id)
#     print(upload_time)
#     print(video_file)
#     print(request)
#     print(request.POST)
#     print(request.FILES)
#     # return HttpResponse(title)
#
#     if title is None or introduction is None or course_id is None or upload_time is None :
#         msg = 'empty input'
#         res = "{\"msg\": \"" + msg + "\"}"
#         return HttpResponse(res)
#
#     try:
#         result = Videos.objects.filter(title = title)
#     except Exception:
#         msg = 'database search video in Vedios error'
#         res = "{\"msg\": \"" + msg + "\"}"
#         return HttpResponse(res)
#     if result:
#         msg = 'video title exit'
#         res = "{\"msg\": \"" + msg + "\"}"
#         return HttpResponse(res)
#
#     video = Videos()
#     video.title = title
#     video.introduction = introduction
#     video.upload_time = datetime.datetime.strptime(upload_time, '%Y-%m-%d %H:%M:%S')
#
#     try:
#         course = Course.objects.filter(id = course_id)
#     except Exception:
#         msg = 'database search course_name in Course error'
#         res = "{\"msg\": \"" + msg + "\"}"
#         return HttpResponse(res)
#     if not course:
#         msg = 'course do not exit'
#         res = "{\"msg\": \"" + msg + "\"}"
#         return HttpResponse(res)
#     video.course_id = course_id
#
#     video_name = title + '.mp4'
#     video_path = os.path.join('/beacon/media', video_name)
#     f = open(video_path, 'wb')
#     for i in video_file.chunks():
#         f.write(i)
#     f.close()
#     video.local_address = '/beacon/media/' + video_name
#
#     clip = VideoFileClip('/beacon/media/' + video_name)
#     video.video_duration = clip.duration
#
#     try:
#         video.save()
#     except Exception:
#         msg = 'database save video error'
#         res = "{\"msg\": \"" + msg + "\"}"
#         return HttpResponse(res)
#
#     msg = 'success'
#     res = "{\"msg\": \"" + msg + "\"}"
#     return HttpResponse(res)


def uploadVideo1(request):
    if (request.method != 'POST'):
        msg = 'fail'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    video_file = request.FILES.get('file')
    # course_id = request.FILES.get('file').name
    print(video_file)
    print(request)
    # return HttpResponse(title)

    if video_file is None :
        msg = 'empty input1'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)


    video = Videos()
    #
    # try:
    #     course = Course.objects.filter(id = course_id)
    # except Exception:
    #     msg = 'database search course_name in Course error'
    #     res = "{\"msg\": \"" + msg + "\"}"
    #     return HttpResponse(res)
    # if not course:
    #     msg = 'course do not exit'
    #     res = "{\"msg\": \"" + msg + "\"}"
    #     return HttpResponse(res)
    # video.course_id = course_id


    video_name = datetime.datetime.now().strftime("%m%d%H%M%S") + '.mp4'
    video_path = os.path.join('/beacon/media', video_name)
    f = open(video_path, 'wb')
    for i in video_file.chunks():
        f.write(i)
    f.close()
    video.local_address = '/beacon/media/' + video_name

    clip = VideoFileClip('/beacon/media/' + video_name)
    video.video_duration = clip.duration

    try:
        video.save()
    except Exception:
        msg = 'database save video error'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    try:
        video = Videos.objects.filter(local_address = '/beacon/media/' + video_name)
    except Exception:
        msg = 'database search local_address in Video error'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    video_id = video[0].id
    res = "{\"msg\": \"success\", \"video_id\": " + str(video_id) + "}"
    return HttpResponse(res)


def uploadVideo2(request):
    if (request.method != 'POST'):
        msg = 'fail'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    dict = request.POST
    title = dict.get('title')
    introduction = dict.get('introduction')
    course_id = dict.get('course_id')
    upload_time = dict.get('upload_time')
    video_id = dict.get('video_id')
    print(title)
    print(introduction)
    print(course_id)
    print(upload_time)
    print(video_id)
    print(request)
    print(request.POST)

    if title is None or introduction is None or course_id is None or upload_time is None or video_id is None:
        msg = 'empty input'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    try:
        video = Videos.objects.filter(id = video_id).first()
    except Exception:
        msg = 'database search video_id in Videos error'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    if not video:
        msg = 'video do not exit'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    video.title = title
    video.introduction = introduction
    video.upload_time = datetime.datetime.strptime(upload_time, '%Y-%m-%d %H:%M:%S')

    try:
        course = Course.objects.filter(id = course_id)
    except Exception:
        msg = 'database search course_name in Course error'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    if not course:
        msg = 'course do not exit'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    video.course_id = course_id

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
    lines = file_data.split('\n')
    i=0
    for line in lines:
        fields = line.split(',')
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
                msg = 'database save userInfo error' + str(i)
                i = i+1
                # res = "{\"msg\": \"" + msg + "\"}"
                res = fields[0]
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
    # url('uploadVideo', uploadVideo),
    url('uploadCourseUser', uploadCourseUser),
    url('uploadVideo1', uploadVideo1),
    url('uploadVideo2', uploadVideo2),
]