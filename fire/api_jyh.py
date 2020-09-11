from django.http import HttpResponse, JsonResponse
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
    videos = Videos.objects.filter(course_id=class_id)

    if(len(videos) == 0):
        msg = '未能找到id为' + class_id + '的课'
        res = '{"message":' + msg +'}'
        return HttpResponse(res)

    videos_send = [x for x in videos.values()]

    send = {}
    send["videos"] = videos_send
    send["message"] = "success"
    
    return JsonResponse(send, safe=False)

url_jyh = [
    url(r'video/play/', getVideo),
]