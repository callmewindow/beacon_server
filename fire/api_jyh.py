from django.http import HttpResponse, JsonResponse
from fire.models import *
from django.conf.urls import url
from django.forms.models import model_to_dict
import time

def getVideo(request):
    if(request.method != 'GET'): 
        msg = '需要GET请求'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    class_id = request.GET.get("class_id", -1)
    if(class_id == -1):
        msg = '需要课程id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)


    # 找到指定的课
    videos = Videos.objects.filter(course_id=class_id)

    if(len(videos) == 0):
        msg = '未能找到id为' + class_id + '的课'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    videos_send = [x for x in videos.values()]

    send = {}
    send["videos"] = videos_send
    send["message"] = "success"
    
    return JsonResponse(send, safe=False)

def openCircle(request):
    if(request.method != 'GET'): 
        msg = '需要GET请求'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    class_id = request.GET.get("class_id", -1)
    if(class_id == -1):
        msg = '需要课程id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    #找到指定的课
    course = None

    try:
        course = Course.objects.get(id = class_id)
    except Exception as e:
        msg = '找不到指定课程'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    #修改字段is_open
    if(course.is_open == 0):
        course.is_open = 1
        course.save()
    else:
        msg = '课程状态异常,' + 'is_open值为' + str(course.is_open)
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    msg = 'success'
    res = '{"message":' + '"' + msg + '"' +'}'
    return HttpResponse(res)

def closeCircle(request):
    if(request.method != 'GET'): 
        msg = '需要GET请求'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    class_id = request.GET.get("class_id", -1)
    if(class_id == -1):
        msg = '需要课程id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    #找到指定的课
    course = None

    try:
        course = Course.objects.get(id = class_id)
    except Exception as e:
        msg = '找不到指定课程'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    #修改字段is_open
    if(course.is_open == 1):
        course.is_open = 0
        course.save()
    else:
        msg = '课程状态异常,' + 'is_open值为' + str(course.is_open)
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    msg = 'success'
    res = '{"message":' + '"' + msg + '"' +'}'
    return HttpResponse(res)

def getClassBasicInfo(request):
    if(request.method != 'GET'): 
        msg = '需要GET请求'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    class_id = request.GET.get("class_id", -1)
    if(class_id == -1):
        msg = '需要课程id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    student_id = request.GET.get("user_id", -1)
    if(student_id == -1):
        msg = '需要学生id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    #找到指定的课
    course = None
    try:
        course = Course.objects.get(id = class_id)
    except Exception as e:
        msg = '找不到指定课程'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    #找信息
    course_name = course.course_name
    course_intro = course.course_intro
    rule = course.rule
    start_time = course.start_time
    end_time = course.end_time
    profession = course.profession
    is_open = course.is_open

    #还要找哪里有观看人数
    person_number = len(UserCourse.objects.filter(course_id = class_id))

    course_info = {}
    course_info["course_name"] = course.course_name
    course_info["course_intro"] = course.course_intro
    course_info["rule"] = course.rule
    course_info["start_time"] = course.start_time
    course_info["end_time"] = course.end_time
    course_info["profession"] = course.profession
    course_info["is_open"] = course.is_open    
    course_info["person_number"] = person_number

    #找一下老师    
    teacher_id = None
    teacher = None
    try:
        #先找到course表里面的老师id
        teacher_id = Course.objects.get(id=class_id).teacher_id_id
        #如果是null,默认第一条
        if(teacher_id == None):
            teacher = Userinfo.objects.get(id=1)
        else:
            #然后去userinfo表里面
            teacher = Userinfo.objects.get(id=teacher_id)
    except Exception as e:
        msg = '找不到老师'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    teacher_name = teacher.realname
    teacher_university = teacher.school
    teacher_profession = teacher.profession
    teacher_email = teacher.email

    send_teacher = {}
    send_teacher["teacher_id"] = teacher_id
    send_teacher["teacher_name"] = teacher_name
    send_teacher["teacher_university"] = teacher_university
    send_teacher["teacher_profession"] = teacher_profession
    send_teacher["teacher_email"] = teacher_email

    #检查一下关系
    relation = -1
    u_v_record = None
    try:
        #查找用户视频记录
        u_v_record = UserCourse.objects.get(course_id=class_id, user_id=student_id)
        relation = u_v_record.user_identity
    except Exception as e:
        relation = 0

    send = {}
    send["course"] = course_info
    send["relation"] = relation
    send["teacher"] = send_teacher
    send["message"] = "success"

    return JsonResponse(send, safe=False)

def authorizeStudent(request):
    if(request.method != 'GET'): 
        msg = '需要GET请求'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    class_id = request.GET.get("class_id", -1)
    if(class_id == -1):
        msg = '需要课程id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
     
    student_id = request.GET.get("student_id", -1)
    if(student_id == -1):
        msg = '需要学生id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)   
    
    op = int(request.GET.get("op", '-1'))
    if(op == -1):
        msg = '需要操作数'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)  
    elif(op != 0 and op != 1):
        msg = '无意义的操作数'
        res = '{"message":' + '"' + msg + '"' +'}'
        res += str(type(op) == type('1'))
        return HttpResponse(res)  

    user_course = UserCourse.objects.filter(course_id = class_id, user_id = student_id)
    if(len(user_course) == 0):
        msg = '未能找到指定课程的用户'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res) 

    for u in user_course:
        if(op == 0):
            u.user_identity = 0
        elif(op == 1):
            u.user_identity = 1
        u.save()

    msg = 'success'
    res = '{"message":' + '"' + msg + '"' +'}'
    return HttpResponse(res)

def searchStudent(request):
    if(request.method != 'GET'): 
        msg = '需要GET请求'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    class_id = request.GET.get("class_id", -1)
    if(class_id == -1):
        msg = '需要课程id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    # 找到指定的记录
    student = UserCourse.objects.filter(course_id=class_id)

    if(len(student) == 0):
        msg = '未能找到本课程学习记录'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    send_u = []

    for s in student:
        send_uu = {}
        user = None

        try:
            #先看看这个在表中存不存在
            user = Userinfo.objects.get(id=s.user_id)
        except Exception as e:
            msg = '不存在id为' + str(s.user_id) + '的用户'
            res = '{"message":' + '"' + msg + '"' +'}'
            return HttpResponse(res)

        send_uu["id"] = s.id
        send_uu["user_id"] = s.user_id
        send_uu["course_id"] = s.course_id
        send_uu["watch_duration"] = s.watch_duration
        send_uu["watch_num"] = s.watch_num
        send_uu["user_identity"] = s.user_identity
        send_uu["activity"] = s.activity
        send_uu["point"] = s.point

        #之后是从userinfo表里查到的数据
        send_uu["username"] = user.username
        send_uu["user_password"] = user.user_password
        send_uu["user_nickname"] = user.user_nickname
        send_uu["introduction"] = user.introduction
        send_uu["user_password"] = user.user_password
        send_uu["phonenumber"] = user.phonenumber
        send_uu["email"] = user.email
        send_uu["qq"] = user.qq
        send_uu["teacher_identity"] = user.teacher_identity
        send_uu["school"] = user.school
        send_uu["school_id"] = user.school_id
        send_uu["realname"] = user.realname
        send_uu["profession"] = user.profession        

        #还要查这个人所相关的课
        records = UserCourse.objects.filter(user_id=s.user_id)
        all_courses = [r.course_id for r in records]

        send_course = []

        #这里遍历每一个课程id
        for a in all_courses:
            c = Course.objects.get(id=a)
            cc = {}
            cc["course_name"] = c.course_name
            cc["course_intro"] = c.course_intro
            cc["rule"] = c.rule
            cc["start_time"] = c.start_time
            cc["end_time"] = c.end_time
            cc["profession"] = c.profession
            cc["is_open"] = c.is_open
            cc["tearcher_id"] = c.teacher_id_id
            send_course += [cc]
            
        # #从course里面找到所有信息
        
        # course = Course.objects.filter(id=s.course_id)

        # for c in course:
        #     cc = {}
        #     cc["course_name"] = c.course_name
        #     cc["course_intro"] = c.course_intro
        #     cc["rule"] = c.rule
        #     cc["start_time"] = c.start_time
        #     cc["end_time"] = c.end_time
        #     cc["profession"] = c.profession
        #     cc["is_open"] = c.is_open
        #     cc["tearcher_id"] = c.teacher_id_id
        #     send_course += [cc]

        send_uu["course"] = send_course

        send_u += [send_uu]
        # send_u += [send_course]
    

    send = {}
    send["students"] = send_u
    send["message"] = "success"
    
    return JsonResponse(send, safe=False)

def addStudent(request):
    if(request.method != 'GET'): 
        msg = '需要GET请求'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    class_id = request.GET.get("class_id", -1)
    if(class_id == -1):
        msg = '需要课程id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    student_id = request.GET.get("student_id", -1)
    if(student_id == -1):
        msg = '需要学生id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    #先看看有没有这条记录
    record = UserCourse.objects.filter(course_id=class_id, user_id=student_id)

    if(len(record) > 0):
        msg = '记录已存在'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    #核实一下class_id和student_id的真实性
    try:
        cond1 = Course.objects.get(id = class_id)
        cond2 = Userinfo.objects.get(id = student_id)
    except Exception as e:
        msg = 'id不合法'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    uc = UserCourse(user_id=student_id, course_id=class_id)
    uc.save()

    msg = 'success'
    res = '{"message":' + '"' + msg + '"' +'}'
    return HttpResponse(res)

def delStudent(request):
    if(request.method != 'GET'): 
        msg = '需要GET请求'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    class_id = request.GET.get("class_id", -1)
    if(class_id == -1):
        msg = '需要课程id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    student_id = request.GET.get("student_id", -1)
    if(student_id == -1):
        msg = '需要学生id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    #先看看有没有这条记录
    record = UserCourse.objects.filter(course_id=class_id, user_id=student_id)

    if(len(record) == 0):
        msg = '记录不存在'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    if(len(record) > 1):
        msg = '学习记录异常，出现重复'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    record.all().delete()
    msg = 'success'
    res = '{"message":' + '"' + msg + '"' +'}'
    return HttpResponse(res)

def updateStudent(request):
    if(request.method != 'POST'): 
        msg = '需要POST请求'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    class_id = request.POST.get("class_id", -1)
    if(class_id == -1):
        msg = '需要课程id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    student_id = request.POST.get("student_id", -1)
    if(student_id == -1):
        msg = '需要学生id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    #找到记录
    record = UserCourse.objects.filter(course_id=class_id, user_id=student_id)

    if(len(record) == 0):
        msg = '记录不存在'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    if(len(record) > 1):
        msg = '学习记录异常，出现重复'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    #以下为非必选项
    watch_duration = request.POST.get("watch_duration", -1)
    if(watch_duration != -1 and type(watch_duration) != type(1)):
        msg = '数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(watch_duration != -1):
        record.watch_duration = watch_duration

    watch_num = request.POST.get("watch_num", -1)
    if(watch_num != -1 and type(watch_num) != type(1)):
        msg = '数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(watch_num != -1):
        record.watch_num = watch_num
    
    activity = request.POST.get("activity", -1)
    if(activity != -1 and type(activity) != type(1)):
        msg = '数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(activity != -1):
        record.activity = activity

    point = request.POST.get("point", -1)
    if(activity != -1 and type(activity) != type(1)):
        msg = '数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(point != -1):
        record.activity = point

    record.save()
    msg = 'success'
    res = '{"message":' + '"' + msg + '"' +'}'
    return HttpResponse(res)

def createCourseApplication(request):
    if(request.method != 'GET'): 
        msg = '需要GET请求'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    class_id = request.GET.get("class_id", -1)
    if(class_id == -1):
        msg = '需要课程id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    student_id = request.GET.get("student_id", -1)
    if(student_id == -1):
        msg = '需要学生id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    content = request.GET.get("content", "")
    if(content == ""):
        msg = '需要content'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


    try:
        ca = CourseApplication(content=content, course_id=class_id, user_id=student_id, application_time=cur_time)
        ca.save()
    except Exception as e:
        msg = 'id不合法'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    

    msg = 'success'
    res = '{"message":' + '"' + msg + '"' +'}'
    return HttpResponse(res)

def updateUser(request):
    if(request.method != 'POST'): 
        msg = '需要POST请求'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    user_id = request.POST.get("user_id", -1)
    if(user_id == -1):
        msg = '需要用户id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    #先找到记录
    user = None
    try:
        user = Userinfo.objects.get(id=user_id)
    except Exception as e:
        msg = '没有该用户id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    #以下为非必须
    username = request.POST.get("username", -1)
    if(username != -1 and type(username) != type("")):
        msg = 'username数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(username != -1):
        user.username = username

    user_password = request.POST.get("user_password", -1)
    if(user_password != -1 and type(user_password) != type("")):
        msg = 'user_password数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(user_password != -1):
        user.user_password = user_password

    user_nickname = request.POST.get("user_nickname", -1)
    if(user_nickname != -1 and type(user_nickname) != type("")):
        msg = 'user_nickname数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(user_nickname != -1):
        user.user_nickname = user_nickname

    introduction = request.POST.get("introduction", -1)
    if(introduction != -1 and type(introduction) != type("")):
        msg = 'introduction数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(introduction != -1):
        user.introduction = introduction

    phonenumber = request.POST.get("phonenumber", -1)
    if(phonenumber != -1 and type(phonenumber) != type("")):
        msg = 'phonenumber数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(phonenumber != -1):
        user.phonenumber = phonenumber

    email = request.POST.get("email", -1)
    if(email != -1 and type(email) != type("")):
        msg = 'email数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(email != -1):
        user.email = email

    qq = request.POST.get("qq", -1)
    if(qq != -1 and type(qq) != type("")):
        msg = 'qq数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(qq != -1):
        user.qq = qq

    teacher_identity = request.POST.get("teacher_identity", -1)
    if(teacher_identity != -1 and type(teacher_identity) != type(1)):
        teacher_id = -1
        try:
            teacher_id = int(teacher_identity)
        except Exception as e:
            msg = 'teacher_identity数据类型错误'
            res = '{"message":' + '"' + msg + '"' +'}'
            return HttpResponse(res)

        if(teacher_id != -1):
            user.teacher_identity = teacher_id

    school = request.POST.get("school", "")
    if(school != "" and type(school) != type("")):
        msg = 'school数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(school != ""):
        user.school = school

    school_id = request.POST.get("school_id", "")
    if(school_id != "" and type(school_id) != type("")):
        msg = 'school_id数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(school_id != ""):
        user.school_id = school_id
    
    realname = request.POST.get("realname", "")
    if(realname != "" and type(realname) != type("")):
        msg = 'realname数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(realname != ""):
        user.realname = realname

    profession = request.POST.get("profession", "")
    if(profession != "" and type(profession) != type("")):
        msg = 'profession数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(profession != ""):
        user.profession = profession

    user.save()
    
    msg = 'success'
    res = '{"message":' + '"' + msg + '"' +'}'

    # res += realname

    return HttpResponse(res)

def searchFriend(request):
    if(request.method != 'GET'): 
        msg = '需要GET请求'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    user_id = request.GET.get("user_id", -1)
    if(user_id == -1):
        msg = '需要用户id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    #判断是不是存在
    try:
        Userinfo.objects.get(id=user_id)
    except Exception as e:
        msg = '用户id不存在'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    send_user = []

    friend1 = FriendRecord.objects.filter(user1_id=user_id)
    for f in friend1:
        #查表找信息
        user = Userinfo.objects.get(id=f.user2_id)
        send_uu = {}
        send_uu["id"] = user.id
        send_uu["username"] = user.username
        send_uu["user_password"] = user.user_password
        send_uu["user_nickname"] = user.user_nickname
        send_uu["introduction"] = user.introduction
        send_uu["user_password"] = user.user_password
        send_uu["phonenumber"] = user.phonenumber
        send_uu["email"] = user.email
        send_uu["qq"] = user.qq
        send_uu["teacher_identity"] = user.teacher_identity
        send_uu["school"] = user.school
        send_uu["school_id"] = user.school_id
        send_uu["realname"] = user.realname
        send_uu["profession"] = user.profession

        #查找他们最后的聊天记录
        last_message = None
        l_message = {}
        try:
            last_message = PrivateMessage.objects.filter(receiver_id=user_id, sender_id=user.id).order_by('-send_time')[0]
        except Exception as identifier:
            pass
        else:
            l_message["content"] = last_message.content
            l_message["send_time"] = last_message.send_time
            l_message["is_read"] = last_message.is_read
            l_message["receiver_id"] = last_message.receiver_id
            l_message["sender_id"] = last_message.sender_id

        send_uu["last_message"] = l_message

        send_user += [send_uu]

    friend2 = FriendRecord.objects.filter(user2_id=user_id)
    for f in friend2:
        #查表找信息
        user = Userinfo.objects.get(id=f.user1_id)
        send_uu = {}
        send_uu["username"] = user.username
        send_uu["user_password"] = user.user_password
        send_uu["user_nickname"] = user.user_nickname
        send_uu["introduction"] = user.introduction
        send_uu["user_password"] = user.user_password
        send_uu["phonenumber"] = user.phonenumber
        send_uu["email"] = user.email
        send_uu["qq"] = user.qq
        send_uu["teacher_identity"] = user.teacher_identity
        send_uu["school"] = user.school
        send_uu["school_id"] = user.school_id
        send_uu["realname"] = user.realname
        send_uu["profession"] = user.profession

        #查找他们最后的聊天记录
        last_message = None
        l_message = {}
        try:
            last_message = PrivateMessage.objects.filter(receiver_id=user_id, sender_id=user.id).order_by('-send_time')[0]
        except Exception as identifier:
            pass
        else:
            l_message["content"] = last_message.content
            l_message["send_time"] = last_message.send_time
            l_message["is_read"] = last_message.is_read
            l_message["receiver_id"] = last_message.receiver_id
            l_message["sender_id"] = last_message.sender_id

        send_uu["last_message"] = l_message

        send_user += [send_uu]

    


    send = {}
    send["message"] = 'success'
    send["users"] = send_user
    return JsonResponse(send, safe=False)

def updateVideo(request):
    if(request.method != 'POST'): 
        msg = '需要POST请求'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    video_id = request.POST.get("video_id", -1)
    if(video_id == -1):
        msg = '需要视频id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    #尝试找一下视频
    video = None
    try:
        video = Videos.objects.get(id=video_id)
    except Exception as e:
        msg = '视频id不合法'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    #以下为非必须
    title = request.POST.get("title", -1)
    if(title != -1 and type(title) != type("")):
        msg = 'title数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(title != -1):
        video.title = title
    
    introduction = request.POST.get("introduction", -1)
    if(introduction != -1 and type(introduction) != type("")):
        msg = 'introduction数据类型错误'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    if(introduction != -1):
        video.introduction = introduction

    video.save()
    
    msg = 'success'
    res = '{"message":' + '"' + msg + '"' +'}'
    return HttpResponse(res)

def deleteVideo(request):
    if(request.method != 'GET'): 
        msg = '需要GET请求'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    video_id = request.GET.get("video_id", -1)
    if(video_id == -1):
        msg = '需要视频id'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    #先看看有没有这条记录
    video = None
    try:
        video = Videos.objects.get(id=video_id)
    except Exception as e:
        msg = '找不到该视频'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    video.delete()
    msg = 'success'
    res = '{"message":' + '"' + msg + '"' +'}'
    return HttpResponse(res)

url_jyh = [
    url(r'video/play/', getVideo),
    url(r'video/manage/update', updateVideo),
    url(r'video/manage/delete', deleteVideo),

    url(r'circle/open/', openCircle),
    url(r'circle/close/', closeCircle),

    url(r'info/basic/class/', getClassBasicInfo),

    url(r'student/manage/authorize/', authorizeStudent),
    url(r'student/manage/search/', searchStudent),
    url(r'student/manage/add/', addStudent),    
    url(r'student/manage/del/', delStudent),    
    url(r'student/manage/update/', updateStudent),

    url(r'class/application/create/', createCourseApplication),

    url(r'user/manage/update/', updateUser),

    url(r'friend/search/', searchFriend),
    
]
