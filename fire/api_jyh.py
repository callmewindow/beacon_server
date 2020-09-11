from django.http import HttpResponse
from fire.models import Videos
from fire.models import Course
from django.conf.urls import url
from django.forms.models import model_to_dict

def getVideo(request):
    if(request.method != 'GET'): 
        msg = '需要GET请求'
        res = '{"message":' + msg +'}'
        return HttpResponse(res)
    
    class_id = request.GET.get("class_id", -1)
    if(class_id == -1):
        msg = '需要课程id'
        res = '{"message":' + msg +'}'
        return HttpResponse(res)

    # 找到指定的课
    course = Course.objects.get(id=class_id)
    # 找到指定课所对应的所有视频
    videos = list(course.video_set.all().values())

    return HttpResponse(videos)

url_jyh = [
    url(r'video/play/', getVideo),
]