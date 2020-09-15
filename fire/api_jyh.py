from django.http import HttpResponse, JsonResponse
from fire.models import *
from django.conf.urls import url
from django.forms.models import model_to_dict
import time
from django.views.decorators.csrf import csrf_exempt

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

    send = {}
    send["course"] = course_info
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

    # student_id = request.GET.get("student_id", -1)
    # if(student_id == -1):
    #     msg = '需要学生id'
    #     res = '{"message":' + '"' + msg + '"' +'}'
    #     return HttpResponse(res)

    # 找到指定的记录
    student = UserCourse.objects.filter(course_id=class_id)

    if(len(student) == 0):
        msg = '未能找到本课程学习记录'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)

    # if(len(student) > 1):
    #     msg = '学习记录异常，出现重复'
    #     res = '{"message":' + '"' + msg + '"' +'}'
    #     return HttpResponse(res)

    student_send = [x for x in student.values()]

    send = {}
    # send["students"] = student_send

    send["students"] = [x for x in student.values()]

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

@csrf_exempt
def createCourseApplication(request):
    if(request.method != 'GET'): 
        msg = '需要GET请求'
        res = '{"message":' + '"' + msg + '"' +'}'
        return HttpResponse(res)
    
    class_id = request.GET.get("class_id", -1)
    if(class_id == -1):
        msg = '需要课程id'
        res = '{"message":' + '"' + msg + '"' +'}'
        res += str(request.POST) 
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

url_jyh = [
    url(r'video/play/', getVideo),
    url(r'circle/open/', openCircle),
    url(r'circle/close/', closeCircle),
    url(r'info/basic/class/', getClassBasicInfo),
    url(r'student/manage/authorize/', authorizeStudent),
    url(r'student/manage/search/', searchStudent),
    url(r'student/manage/add/', addStudent),    
    url(r'student/manage/del/', delStudent),    
    url(r'student/manage/update/', updateStudent),
    url(r'class/application/create/', createCourseApplication),
]
