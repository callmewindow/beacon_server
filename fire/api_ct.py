from django.shortcuts import render
from fire.models import *
from django.http.response import HttpResponse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.db.models import Max 


#获取帖子信息，包括帖子的"标题"、"发帖人"、"发帖时间"、"内容"、"点赞(like)数"，以及该帖子下的所有"回复"。回复包括每条回复的"内容"、"回复人"、"时间"
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
        topped = str((floor_1_res.topped))
        watches = str((post_res.watches))
        stared = str((floor_1_res.stared))
        reply = Floor.objects.filter(post_id=post_id).values("id","content","userinfo__username","post_time","floor_num")
        reply_list = []
        for i in reply:
            tmp = {'id':i.id, 'content':i.content, 'author':i.userinfo__unsername, 'datetime':str(i.post_time), 'floor':str(i.floor_num)}
            reply_list.append(tmp)

        content = {'title': post_res.title, 'author':post_author, 'datetime':post_time, 'content':post_content, 'read':watches, 'like':like_num, 'top':topped, 'highlight':stared, 'reply_list':reply}
        return JsonResponse(content)


#回复帖子
def replyPost(request):
    if(request.method!='POST'):
        return None
    dict = request.GET
    post_id = dict.get('postId')
    author_id = dict.get('author')
    reply_content = dict.get('content')
    reply_time = dict.get('datetime')
    floor_num = dict.get('floor')
    try:
        new_reply = Floor.objects.create(author_id=author_id, post_id=post_id, content=reply_content, post_time=reply_time, floor_num=floor_num)
        res = 'ok'
    except Exception:
        res = 'api_ct replyPost error'
    if(res = 'api_ct replyPost error'):
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
    dict = request.GET
    cicle_id = dict.get('forumId')
    try:
        res = Post.objects.filter(course_id=cicle_id)
    except Exception:
        post_res = 'api_ct cicleAllPost error'
    if (post_res=='api_ct cicleAllPost error'):
        err_msg = "api_ct cicleAllPost error."
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2) 
    else:
        post_list = []
        for i in res:
            author_name = Userinfo.objects.filter(id=i.id).username
            floor_1_res = Floor.objects.filter(Q(post_id=i.id) & Q(floor_num =1))
            reply_num = Floor.objects.filter(post_id=i.id).aggregate(Max('floor_num')).floor_num__max-1
            content = {'id':str(i.id), 'title':i.title, 'author':author_name, 'datetime':str(floor_1_res.post_time), 'content':floor_1_res.content, 'read':str(i.watches), 'like':str(floor_1_res.like_num), 'reply_num':reply_num ,'top':str(i.topped) ,'highlight':str(i.stared)}
            post_list.append(content)
        #msg = "{\"msg\":\"ok\"" + "\"post_list\"" + "\""+ post_list+ "\"" +"}"\
        #res_dict = {'msg':'ok', 'post_list':post_list}
        return JsonResponse(post_list)




url_ct = [
	url('/getPostInfo',getPostInfo),
    url('/replyPost',replyPost),
    url('/cicleAllPost',cicleAllPost),
	
	]