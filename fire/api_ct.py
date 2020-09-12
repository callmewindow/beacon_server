from django.shortcuts import render
from fire.models import *
from django.http.response import HttpResponse
from django.forms.models import model_to_dict
from django.http import JsonResponse
<<<<<<< HEAD
from django.conf.urls import url
=======
from django.db.models import Max 
from django.conf.urls import url
from django.db.models import Q
from itertools import chain
import datetime

>>>>>>> 72626f8a5d84e22dc9467f6fb04e33bb8fda0b71

#获取帖子信息，包括帖子的"标题"、"发帖人"、"发帖时间"、"内容"、"点赞(like)数"，以及该帖子下的所有"回复"。回复包括每条回复的"内容"、"回复人"、"时间"
# def getPostInfo(request):
#     if(request.method!='POST'):
#         return None
#     dict = request.POST
#     post_id = dict.get('postId')
#     post_res = Post.objects.filter(id=post_id)
    
#     if post_res:
#         floor_1_res = Floor.objects.filter(Q(post_id=post_id) & Q(floor_num =1))
#         post_author = Post.objects.filter(id=post_id).values("owner_id__username")
#         post_time = str(floor_1_res[0].post_time)
#         post_content = floor_1_res[0].content
#         like_num = str(floor_1_res[0].like_num)
#         topped = str((post_res[0].topped))
#         watches = str((post_res[0].watches))
#         stared = str((post_res[0].stared))
#         reply = Floor.objects.filter(post_id=post_id).values("id","content","author_id__username","post_time","floor_num")
#         reply_list = []
#         for i in reply:
#             # tmp = {'id':i.id, 'content':i.content, 'author':i.userinfo__unsername, 'datetime':str(i.post_time), 'floor':str(i.floor_num)}
#             # reply_list.append(tmp)
#             return HttpResponse(i)

#         # content = {'title': post_res.title, 'author':post_author[0], 'datetime':post_time, 'content':post_content, 'read':watches, 'like':like_num, 'top':topped, 'highlight':stared, 'reply_list':reply}
#         # return JsonResponse(content)
#     else:
#         err_msg = "api_ct getPostInfo error."
#         msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
#         return HttpResponse(msg2) 


#回复帖子
def replyPost(request):
    if(request.method!='POST'):
        return None
    dict = request.POST
    post_id = dict.get('postId')
    author_id = dict.get('author_id')
    reply_content = dict.get('content')
    # reply_time = dict.get('datetime')
    # floor_num = dict.get('floor')
    reply_time = datetime.datetime.now()
    floor_list = Floor.objects.filter(post_id=post_id)
    if floor_list:
        floor_num = 0
        for i in floor_list:
            floor_num = floor_num+1
        floor_num = floor_num+1
    else:
         return HttpResponse('没有这个post_id') 

    try:
        floor = Floor()
        floor.content = reply_content
        floor.post_time = reply_time
        floor.floor_num = floor_num
        floor.reply_floor = 0
        floor.like_num = 0
        floor.author_id = author_id
        floor.post_id = post_id
        #new_reply = Floor.objects.create(author_id=author_id, post_id=post_id, content=str(reply_content), post_time=reply_time, floor_num=floor_num,like_num=0,reply_floor=0)
        floor.save()
        res = 'ok'
    except Exception:
        res = 'api_ct replyPost error'
    if(res == 'api_ct replyPost error'):
        err_msg = "api_ct replyPost error."
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2) 
    else:
        msg = "ok"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2) 

#显示圈子下的所有帖子
def cicleAllPost(request):
    if(request.method!='POST'):
        return None
    dict = request.POST
    cicle_id = dict.get('forumId')
    res = Post.objects.filter(course_id=cicle_id)
    if res:
        post_list = []
        for i in res:
            author_name = Userinfo.objects.filter(id=i.owner_id)[0].username
            floor_1_res = Floor.objects.filter(Q(post_id=i.id) & Q(floor_num =1))
            datetime = floor_1_res[0].post_time
            content = floor_1_res[0].content
            watches = i.watches
            like_num = floor_1_res[0].like_num
            if i.topped:
                topped = str(i.topped)
            else:
                topped = 'null'
            if i.stared:
                stared = str(i.stared)
            else:
                stared = 'null'
            floor_list = Floor.objects.filter(post_id=i.id)
            reply_num = 0
            for x in floor_list:
                reply_num = reply_num+1
            reply_num = reply_num-1
            

                
            content = {'id':str(i.id), 'title':i.title, 'author':author_name, 'datetime':str(datetime), 'content':content, 'read':str(watches), 'like':str(like_num), 'reply_num':reply_num ,'top':topped ,'highlight':stared}
            post_list.append(content)
        #msg = "{\"msg\":\"ok\"" + "\"post_list\"" + "\""+ post_list+ "\"" +"}"\
        #res_dict = {'msg':'ok', 'post_list':post_list}
        return JsonResponse(post_list,safe=False)
    else:
        return HttpResponse('该圈子id不存在') 
        




url_ct = [
<<<<<<< HEAD
	url('getPostInfo',getPostInfo),
=======
	#url('getPostInfo',getPostInfo),
    url('replyPost',replyPost),
    url('cicleAllPost',cicleAllPost),
>>>>>>> 72626f8a5d84e22dc9467f6fb04e33bb8fda0b71
	
	]