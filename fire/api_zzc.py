import json
from builtins import type, eval, Exception, range, int, sorted

from django.shortcuts import render
from fire.models import *
from django.http.response import HttpResponse
import datetime
import os
from moviepy.editor import VideoFileClip
from django.conf.urls import url
import xlrd
import xlwt


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

    msg = 'success'
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
def uploadUserCourse1(request):
    if (request.method != 'POST'):
        msg = 'fail'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    excel_file = request.FILES.get('file')
    excel_name = request.FILES.get('file').name
    # course_name = request.POST.get('course_name')
    # course_id = request.POST.get('course_id')
    # print(request)
    # print(request.FILES)
    # print(request.FILES.get('file'))
    # print(request.FILES.get('file').name)
    # print(request.POST)
    # print(request.POST.get('file'))

    if excel_file is None:
        msg = 'empty input'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    # if not csv_file.name.endswith('.csv'):
    #     msg = 'file is not csv type'
    #     res = "{\"msg\": \"" + msg + "\"}"
    #     return HttpResponse(res)

    excel_path = os.path.join('/beacon/excel', excel_name)
    f = open(excel_path, 'wb')
    for i in excel_file.chunks():
        f.write(i)
    f.close()

    return HttpResponse(excel_name)


def uploadUserCourse2(request):
    if (request.method != 'POST'):
        msg = 'fail'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    course_id = int(request.POST.get('course_id'))
    excel_name = request.POST.get('excel_name')

    print(type(course_id))
    print(course_id)
    print(excel_name)
    if course_id is None or excel_name is None:
        return HttpResponse("empty input")

    # print(os.path.join("/beacon/excel", excel_name))
    # print(excel_name)

    excel_path = os.path.join('/beacon/excel', excel_name)
    try:
        table = xlrd.open_workbook(excel_path, encoding_override='utf-8')
    except Exception as Argument:
        return HttpResponse(Argument)
        msg = 'open excel error'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    #remember to delete at last

    sheet = table.sheets()[0]

    # user_id_list = []
    for i in range(1, sheet.nrows):
        row_value = sheet.row_values(i)
        print(row_value)
        print(row_value[0])
        email = row_value[3]

        try:
            user = Userinfo.objects.filter(email=email).first()
        except Exception:
            msg = 'database search email in UserInfo error'
            res = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(res)
        if not user:
            userinfo = Userinfo()
            userinfo.username = row_value[3]
            userinfo.school = row_value[0]
            userinfo.school_id = row_value[1]
            userinfo.realname = row_value[2]
            userinfo.email = row_value[3]
            try:
                userinfo.save()
            except Exception:
                msg = 'database save userInfo error'
                res = "{\"msg\": \"" + msg + "\"}"
                return HttpResponse(res)
        # user = UserCourse.objects.filter(realname=realname)
        # return HttpResponse(user + user.first())
        else:
            if user.school is not row_value[0] or user.school_id is not row_value[1] or user.realname is not row_value[2]:
                continue

        try:
            userInUserinfo = Userinfo.objects.filter(email=email).first()
        except Exception:
            msg = 'database search email in Userinfo error'
            res = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(res)
        user_id = userInUserinfo.id
        # try:
        #     userInUserCourse = UserCourse.objects.filter(user_id=user_id).first()
        # except Exception:
        #     msg = 'database search realname in UserCourse error'
        #     res = "{\"msg\": \"" + msg + "\"}"
        #     return HttpResponse(res)
        # if not userInUserCourse:
        #     userCourse = UserCourse()
        #     userCourse.user_id = user_id
        #     userCourse.user_identity = 0  # 每日任务-共享信息
        #     try:
        #         userCourse.save()
        #     except Exception:
        #         msg = 'database save userCourse error'
        #         res = "{\"msg\": \"" + msg + "\"}"
        #         return HttpResponse(res)
        # user_id_list.append(user_id)

        try:
            userInUserCourse = UserCourse.objects.filter(user_id=user_id, course_id=course_id).first()
        except Exception:
            msg = 'database search user_id and course_id in UserCourse error'
            res = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(res)
        if not userInUserCourse:
            userCourse = UserCourse()
            userCourse.user_id = user_id
            userCourse.course_id = course_id
            userCourse.user_identity = 0  # 每日任务-共享信息
            try:
                userCourse.save()
            except Exception:
                msg = 'database save userCourse error'
                res = "{\"msg\": \"" + msg + "\"}"
                return HttpResponse(res)

    # file_data = csv_file.read().decode('gb2312', 'ignore')
    # lines = file_data.split('\n')
    # i=0
    # for line in lines[1:]:
    #     fields = line.split(',')
    #     realname = fields[2]
    #
    #     try:
    #         user = Userinfo.objects.filter(realname = realname)
    #     except Exception:
    #         msg = 'database search realname in UserInfo error'
    #         res = "{\"msg\": \"" + msg + "\"}"
    #         return HttpResponse(res)
    #     if not user:
    #         userInfo = Userinfo()
    #         userInfo.school = fields[0]
    #         userInfo.school_id = fields[1]
    #         userInfo.realname = fields[2]
    #         userInfo.email = fields[3]
    #         print(fields[0])
    #         print(fields[1])
    #         print(fields[2])
    #         print(fields[3])
    #         print(userInfo.school)
    #         print(userInfo.school_id)
    #         print(userInfo.realname)
    #         print(userInfo.email)
    #         # try:
    #         #     userInfo.save()
    #         # except Exception:
    #         #     msg = 'database save userInfo error' + str(i)
    #         #     res = "{\"msg\": \"" + msg + "\"}"
    #         #     # res = fields[0]
    #         #     return HttpResponse(res)
    #         userInfo.save()
    #     # user = UserCourse.objects.filter(realname=realname)
    #     # return HttpResponse(user + user.first())
    #     try:
    #         userInUserinfo = Userinfo.objects.filter(realname = realname).first()
    #     except Exception:
    #         msg = 'database search realname in Userinfo error'
    #         res = "{\"msg\": \"" + msg + "\"}"
    #         return HttpResponse(res)
    #     user_id = userInUserinfo.id
    #     try:
    #         userInUserCourse = UserCourse.objects.filter(user_id = user_id).first()
    #     except Exception:
    #         msg = 'database search realname in UserCourse error'
    #         res = "{\"msg\": \"" + msg + "\"}"
    #         return HttpResponse(res)
    #     if not userInUserCourse:
    #         userCourse = UserCourse()
    #         userCourse.user_id = user_id
    #         userCourse.course_id = course_id
    #         userCourse.user_identity = 0 #每日任务-共享信息
    #         try:
    #             userCourse.save()
    #         except Exception:
    #             msg = 'database save userCourse error'
    #             res = "{\"msg\": \"" + msg + "\"}"
    #             return HttpResponse(res)
    #
    #     i = i + 1

    os.remove(excel_path)

    msg = 'success'
    res = "{\"msg\": \"" + msg + "\"}"
    return HttpResponse(res)



# def uploadUserCourse2(request):
#     if (request.method != 'POST'):
#         msg = 'fail'
#         res = "{\"msg\": \"" + msg + "\"}"
#         return HttpResponse(res)
#     user_id_list = request.POST.get('user_id_list')
#     course_id = request.POST.get('course_id')
#
#     for user_id in user_id_list:
#         try:
#             userInUserCourse = UserCourse.objects.filter(user_id=user_id, course_id=course_id).first()
#         except Exception:
#             msg = 'database search user_id and course_id in UserCourse error'
#             res = "{\"msg\": \"" + msg + "\"}"
#             return HttpResponse(res)
#         if not userInUserCourse:
#             userCourse = UserCourse()
#             userCourse.user_id = user_id
#             userCourse.course_id = course_id
#             userCourse.user_identity = 0  # 每日任务-共享信息
#             try:
#                 userCourse.save()
#             except Exception:
#                 msg = 'database save userCourse error1'
#                 res = "{\"msg\": \"" + msg + "\"}"
#                 return HttpResponse(res)
#         else:
#             if userInUserCourse.course_id is not course_id or
#             userInUserCourse.course_id = course_id
#             try:
#                 userInUserCourse.save()
#             except Exception:
#                 msg = 'database save userCourse error2'
#                 res = "{\"msg\": \"" + msg + "\"}"
#                 return HttpResponse(res)
#
#     return HttpResponse('tmp_return')



# 查看并发送好友私信：作为平台用户，我希望和已经是好友的平台成员发送私信并看到对方的。————维护消息数据表



def getPrivateMessages(request):
    if (request.method != 'POST'):
        msg = 'fail'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    dict = request.POST
    user_id1 = dict.get('user_id1')
    user_id2 = dict.get('user_id2')

    if user_id1 is None or user_id2 is None:
        msg = 'empty input'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    try:
        privateMessages = PrivateMessage.objects.filter(sender_id=user_id1, receiver_id=user_id2)
    except Exception:
        msg = 'database search sender_id and receiver_id in PrivateMessage error1'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    flag = 0
    result = []
    if not privateMessages:
        flag = 1
    else:
        for privateMessage in privateMessages:
            send_time = datetime.datetime.strftime(privateMessage.send_time, '%Y-%m-%d %H:%M:%S')
            one_message = {}
            one_message["sender_id"] = privateMessage.sender_id
            one_message["content"] = privateMessage.content
            one_message["send_time"] = send_time
            result.append(one_message)
            privateMessage.is_read = 1
            privateMessage.save()
    print(result)
    try:
        privateMessages2 = PrivateMessage.objects.filter(sender_id=user_id2, receiver_id=user_id1)
    except Exception:
        msg = 'database search sender_id and receiver_id in PrivateMessage error2'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    print(privateMessages)
    if not privateMessages2:
        if flag == 1:
            msg = 'empty privateMessage'
            res = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(res)
        else:
            result = sorted(result, key=lambda keys: keys['send_time'])
            # result.sort(key=send_time)
            # res = "{\"result\":" + str(result) + "}"
            # return HttpResponse(res)
            return HttpResponse(json.dumps(result))
    else:
        for privateMessage in privateMessages2:
            send_time = datetime.datetime.strftime(privateMessage.send_time, '%Y-%m-%d %H:%M:%S')
            one_message = {}
            one_message["sender_id"] = privateMessage.sender_id
            one_message["content"] = privateMessage.content
            one_message["send_time"] = send_time
            result.append(one_message)
            privateMessage.is_read = 1
            privateMessage.save()
            print(result)
        result = sorted(result, key=lambda keys: keys['send_time'])
        # result.sort(key=send_time)
        # res = "{\"result\":" + str(result) + "}"
        # return HttpResponse(res)
        return HttpResponse(json.dumps(result))



# def getPrivateMessage(request):
#     if (request.method != 'POST'):
#         msg = 'fail'
#         res = "{\"msg\": \"" + msg + "\"}"
#         return HttpResponse(res)
#     dict = request.POST
#     sender_id = dict.get('sender_id')
#     receiver_id = dict.get('receiver_id')
#     send_time = dict.get('send_time')
#
#     if sender_id is None or receiver_id is None or send_time is None:
#         msg = 'empty input'
#         res = "{\"msg\": \"" + msg + "\"}"
#         return HttpResponse(res)
#
#     try:
#         privateMessage = PrivateMessage.objects.filter(sender=sender_id, receiver=receiver_id, send_time=send_time)
#     except:
#         msg = 'database search sender_id, receiver_id and send_time in PrivateMessage error'
#         res = "{\"msg\": \"" + msg + "\"}"
#         return HttpResponse(res)
#     if not privateMessage:
#         msg = 'privateMessage do not exist'
#         res = "{\"msg\": \"" + msg + "\"}"
#         return HttpResponse(res)
#     content = privateMessage.content
#
#     return HttpResponse(content)



def postPrivateMessage(request):
    if (request.method != 'POST'):
        msg = 'fail'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    dict = request.POST
    sender_id = dict.get('sender_id')
    receiver_id = dict.get('receiver_id')
    content = dict.get('content')
    send_time = dict.get('send_time')

    if sender_id is None or receiver_id is None or content is None or send_time is None:
        msg = 'empty input'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    privateMessage = PrivateMessage()
    privateMessage.sender_id = sender_id
    privateMessage.receiver_id = receiver_id
    privateMessage.content = content
    privateMessage.send_time = datetime.datetime.strptime(send_time, '%Y-%m-%d %H:%M:%S')
    privateMessage.is_read = 0
    try:
        privateMessage.save()
    except:
        msg = 'database save privateMessage error'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    msg = 'success'
    res = "{\"msg\": \"" + msg + "\"}"
    return HttpResponse(res)



def sendFriendApplication(request):
    if (request.method != 'POST'):
        msg = 'fail'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    dict = request.POST
    




url_zzc = [
    url('createCourse', createCourse),
    # url('uploadVideo', uploadVideo),
    url('uploadVideo1', uploadVideo1),
    url('uploadVideo2', uploadVideo2),
    # url('uploadUserCourse', uploadUserCourse),
    url('uploadUserCourse1', uploadUserCourse1),
    url('uploadUserCourse2', uploadUserCourse2),
    url('getPrivateMessages', getPrivateMessages),
    # url('getPrivateMessage', getPrivateMessage),
    url('postPrivateMessage', postPrivateMessage),
    url('sendFriendApplication', sendFriendApplication),
]