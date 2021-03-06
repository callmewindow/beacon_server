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
import traceback


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

    dict = request.POST
    course_name=dict.get('course_name')
    course_intro=dict.get('course_intro')
    # rule=dict.get('rule')
    start_time=dict.get('start_time')
    end_time=dict.get('end_time')
    profession=dict.get('profession')
    teacher_id = dict.get('teacher_id')

    course=Course()
    course.course_name=course_name
    course.course_intro=course_intro
    # course.rule=rule
    course.start_time=datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    course.end_time=datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    course.profession=profession
    course.teacher_id_id = teacher_id

    try:
        course.save()
    except Exception:
        msg = 'database save course error'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    msg = 'success'
    res = "{\"msg\": \"" + msg + "\"}"
    return HttpResponse(res)



def uploadVideo1(request):
    if (request.method != 'POST'):
        msg = 'fail'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    video_file = request.FILES.get('file')
    print(video_file)
    print(request)

    if video_file is None :
        msg = 'empty input1'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    video = Videos()

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

    if excel_file is None:
        msg = 'empty input'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

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

    if course_id is None or excel_name is None:
        return HttpResponse("empty input")

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
            userinfo.school_id = str(int(row_value[1]))
            userinfo.realname = row_value[2]
            userinfo.email = row_value[3]
            userinfo.user_password = 'beacon123'
            userinfo.user_nickname = row_value[3]
            try:
                userinfo.save()
            except Exception:
                msg = 'database save userInfo error'
                res = "{\"msg\": \"" + msg + "\"}"
                return HttpResponse(res)
        else:
            if user.school != row_value[0] or user.school_id != str(int(row_value[1])) or user.realname != row_value[2]:
                continue

        try:
            userInUserinfo = Userinfo.objects.filter(email=email).first()
        except Exception:
            msg = 'database search email in Userinfo error'
            res = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(res)
        user_id = userInUserinfo.id

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
            userCourse.point = 0
            userCourse.watch_duration = 0
            userCourse.watch_num = 0
            try:
                userCourse.save()
            except Exception:
                msg = 'database save userCourse error'
                res = "{\"msg\": \"" + msg + "\"}"
                return HttpResponse(res)

    os.remove(excel_path)

    msg = 'success'
    res = "{\"msg\": \"" + msg + "\"}"
    return HttpResponse(res)



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
            return HttpResponse(json.dumps(result, ensure_ascii=False))
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
        return HttpResponse(json.dumps(result))



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



def json_raw(dict):
	return str(dict).replace('\'','\"').replace('None','null')

def sendFriendApplication(request):
    try:
        msg = {}
        if (request.method != 'POST'):
            msg['result'] = 'not post'
            return HttpResponse(json_raw(msg))
        dict = request.POST
        applicant_id = dict.get('applicant_id')
        target_id = dict.get('target_id')
        application_content = dict.get('application_content') # spell correctly
        application_time = dict.get('application_time')

        if applicant_id is None:
            msg['result'] = 'empty applicant_id'
            return HttpResponse(json_raw(msg))
        if target_id is None:
            msg['result'] = 'empty target_id'
            return HttpResponse(json_raw(msg))
        if application_content is None:
            msg['result'] = 'empty application_content'
            return HttpResponse(json_raw(msg))
        if application_time is None:
            msg['result'] = 'empty application time'
            return HttpResponse(json_raw(msg))

        friend_record1 = FriendRecord.objects.filter(user1_id=applicant_id, user2_id=target_id)
        friend_record2 = FriendRecord.objects.filter(user1_id=target_id, user2_id=applicant_id)
        if friend_record1 or friend_record2:
            msg['result'] = 'already friend'
            return HttpResponse(json_raw(msg))

        friendApplication = FriendApplication.objects.filter(applicant_id=applicant_id, target_id=target_id)
        if friendApplication:
            msg['result'] = 'already applied'
            return HttpResponse(json_raw(msg))
        friendApplication = FriendApplication()
        friendApplication.applicant_id = applicant_id
        friendApplication.target_id = target_id
        friendApplication.application_content = application_content
        friendApplication.application_time = datetime.datetime.strptime(application_time, '%Y-%m-%d %H:%M:%S')
        friendApplication.save()
        # userinfo = Userinfo.objects.filter(id=applicant_id).first()
        # msg['username'] = userinfo.username
        # msg['user_nickname'] = userinfo.user_nickname
        # msg['applicant_id'] = applicant_id
        msg['result'] = 'success'
        return HttpResponse(json_raw(msg))
    except:
        traceback.print_exc()
        msg['result'] = 'Unexpected Error'
        return HttpResponse(json_raw(msg))



def passFriendApplication(request):
    try:
        msg = {}
        if (request.method != 'POST'):
            msg['result'] = 'not post'
            return HttpResponse(json_raw(msg))
        dict = request.POST
        applicant_id = dict.get('applicant_id')
        target_id = dict.get('target_id')

        if applicant_id is None:
            msg['result'] = 'empty applicant_id'
            return HttpResponse(json_raw(msg))
        if target_id is None:
            msg['result'] = 'empty target_id'
            return HttpResponse(json_raw(msg))

        friendApplication = FriendApplication.objects.filter(applicant_id=applicant_id, target_id=target_id).first()
        if not friendApplication:
            msg['result'] = 'no friend application'
            return HttpResponse(json_raw(msg))
        friendApplication.result = 1
        friendApplication.save()
        friendRecord = FriendRecord()
        friendRecord.user1_id = applicant_id
        friendRecord.user2_id = target_id
        friendRecord.save()
        msg['result'] = 'success'
        return HttpResponse(json_raw(msg))
    except:
        traceback.print_exc()
        msg['result'] = 'Unexpected Error'
        return HttpResponse(json_raw(msg))



def rejectFriendApplication(request):
    try:
        msg = {}
        if (request.method != 'POST'):
            msg['result'] = 'not post'
            return HttpResponse(json_raw(msg))
        dict = request.POST
        applicant_id = dict.get('applicant_id')
        target_id = dict.get('target_id')

        if applicant_id is None:
            msg['result'] = 'empty applicant_id'
            return HttpResponse(json_raw(msg))
        if target_id is None:
            msg['result'] = 'empty target_id'
            return HttpResponse(json_raw(msg))

        friendApplication = FriendApplication.objects.filter(applicant_id=applicant_id, target_id=target_id).first()
        if not friendApplication:
            msg['result'] = 'no friend application'
            return HttpResponse(json_raw(msg))
        friendApplication.result = 2
        friendApplication.save()
        msg['result'] = 'success'
        return HttpResponse(json_raw(msg))
    except:
        traceback.print_exc()
        msg['result'] = 'Unexpected Error'
        return HttpResponse(json_raw(msg))



def getFriendApplicationOfYourself(request):
    try:
        msg = {}
        if (request.method != 'POST'):
            msg['result'] = 'not post'
            return HttpResponse(json_raw(msg))
        dict = request.POST
        applicant_id = dict.get('applicant_id')

        if applicant_id is None:
            msg['result'] = 'empty applicant_id'
            return HttpResponse(json_raw(msg))

        friendApplications = FriendApplication.objects.filter(applicant_id=applicant_id)
        if not friendApplications:
            msg['result'] = 'no friend application'
            return HttpResponse(json_raw(msg))
        applications = []
        for friendApplication in friendApplications:
            one_application = {}
            one_application['application_content'] = friendApplication.application_content
            one_application['application_time'] = datetime.datetime.strftime(friendApplication.application_time, '%Y-%m-%d %H:%M:%S')
            one_application['result'] = friendApplication.result
            target_id = friendApplication.target_id
            userinfo = Userinfo.objects.filter(id=target_id).first()
            one_application['username'] = userinfo.username
            one_application['user_nickname'] = userinfo.user_nickname
            one_application['target_id'] = target_id
            applications.append(one_application)
        return HttpResponse(json.dumps(applications, ensure_ascii=False))
    except:
        traceback.print_exc()
        msg['result'] = 'Unexpected Error'
        return HttpResponse(json_raw(msg))



def getFriendApplicationOfOthers(request):
    try:
        msg = {}
        if (request.method != 'POST'):
            msg['result'] = 'not post'
            return HttpResponse(json_raw(msg))
        dict = request.POST
        target_id = dict.get('target_id')

        if target_id is None:
            msg['result'] = 'empty target_id'
            return HttpResponse(json_raw(msg))

        friendApplications = FriendApplication.objects.filter(target_id=target_id)
        if not friendApplications:
            msg['result'] = 'no friend application'
            return HttpResponse(json_raw(msg))
        applications = []
        for friendApplication in friendApplications:
            one_application = {}
            one_application['application_content'] = friendApplication.application_content
            one_application['application_time'] = datetime.datetime.strftime(friendApplication.application_time, '%Y-%m-%d %H:%M:%S')
            one_application['result'] = friendApplication.result
            applicant_id = friendApplication.applicant_id
            userinfo = Userinfo.objects.filter(id=applicant_id).first()
            one_application['username'] = userinfo.username
            one_application['user_nickname'] = userinfo.user_nickname
            one_application['applicant_id'] = applicant_id
            applications.append(one_application)
        return HttpResponse(json.dumps(applications, ensure_ascii=False))
    except:
        traceback.print_exc()
        msg['result'] = 'Unexpected Error'
        return HttpResponse(json_raw(msg))



def deleteFriendRecord(request):
    try:
        msg = {}
        if (request.method != 'POST'):
            msg['result'] = 'not post'
            return HttpResponse(json_raw(msg))
        dict = request.POST
        user1_id = dict.get('user1_id')
        user2_id = dict.get('user2_id')

        if user1_id is None:
            msg['result'] = 'empty user1_id'
            return HttpResponse(json_raw(msg))
        if user2_id is None:
            msg['result'] = 'empty user2_id'
            return HttpResponse(json_raw(msg))

        friendRecord = FriendRecord.objects.filter(user1_id=user1_id, user2_id=user2_id)
        if not friendRecord:
            msg['result'] = 'empty friend record'
            return HttpResponse(json_raw(msg))
        FriendRecord.objects.filter(user1_id=user1_id, user2_id=user2_id).delete()
        msg['result'] = 'success'
        return HttpResponse(json_raw(msg))
    except:
        traceback.print_exc()
        msg['result'] = 'Unexpected Error'
        return HttpResponse(json_raw(msg))



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
    url('passFriendApplication', passFriendApplication),
    url('rejectFriendApplication', rejectFriendApplication),
    url('getFriendApplicationOfYourself', getFriendApplicationOfYourself),
    url('getFriendApplicationOfOthers', getFriendApplicationOfOthers),
    url('deleteFriendRecord', deleteFriendRecord),
]