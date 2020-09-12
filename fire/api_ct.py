from django.shortcuts import render
from fire.models import *
from django.http.response import HttpResponse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.conf.urls import url

def getPostInfo(request):
    if(request.method!='GET'):
        return None
    dict = request.GET
    post_id = dict.get('postId')
    try:
        post_res = Post.objects.filter(id=post_id)
    except Exception:
        post_res = 'api_ct getPostInfo error'
    if (post_res=='api_ct getPostInfo error'):
        err_msg = "api_ct getPostInfo error."
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2) 
    else :
        
        floor_1_res = Floor.objects.filter(Q(post_id=post_id) & Q(floor_num =1))
        post_author = Post.objects.filter(id=post_id).values("userinfo__unsername")
        post_time = str(floor_1_res.post_time)
        post_content = floor_1_res.content
        like_num = str(floor_1_res.like_num)
        reply = Floor.objects.filter(post_id=post_id).values_list("content","userinfo__username","post_time")

        content = {'msg':'ok', '标题': post_res.title, '发帖人':post_author, '发帖时间':post_time, '内容':post_content, '点赞数':like_num, '回复':reply}
        return JsonResponse(content)


url_ct = [
	url('getPostInfo',getPostInfo),
	
	]