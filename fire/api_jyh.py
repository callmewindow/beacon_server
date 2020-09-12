from django.http import HttpResponse, JsonResponse
from fire.models import *
from django.conf.urls import url
from django.forms.models import model_to_dict

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
    course = Course.objects.get(id = class_id)
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

    course_info = {}
    course_info["course_name"] = course.course_name
    course_info["course_intro"] = course.course_intro
    course_info["rule"] = course.rule
    course_info["start_time"] = course.start_time
    course_info["end_time"] = course.end_time
    course_info["profession"] = course.profession
    course_info["is_open"] = course.is_open    

    send = {}
    send["course"] = course_info
    send["message"] = "success"

    return JsonResponse(send, safe=False)

url_jyh = [
    url(r'video/play/', getVideo),
    url(r'circle/open/', openCircle),
    url(r'info/basic/class/', getClassBasicInfo),
]
