from django.shortcuts import render
from fire.models import *
from django.http.response import HttpResponse
import datetime
from django.conf.urls import url

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
        msg = 'database search course_name error'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    if result:
        msg = 'existCourseName'
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

url_zzc = [
    url('api/course/createCourse', course.createCourse),
]