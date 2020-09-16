from django.shortcuts import render
from fire.models import *
from django.http.response import HttpResponse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.conf.urls import url
from django.db.models import Max 
from django.conf.urls import url
from django.db.models import Q
from itertools import chain
import datetime
import operator


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
            nickname = Userinfo.objects.filter(id=i.owner_id)[0].user_nickname
            if nickname:
                nickname = nickname
            else:
                nickname = 'null'
            teacher_identity = Userinfo.objects.filter(id=i.owner_id)[0].teacher_identity
            if teacher_identity:
                teacher_identity = str(teacher_identity)
            else:
                teacher_identity = 'null'
            floor_1_res = Floor.objects.filter(Q(post_id=i.id) & Q(floor_num =1))


            floor_res = Floor.objects.filter(post_id=i.id)
            tmp_list = []
            for x in floor_res:
                last_time = str(x.post_time)
                last_name = Userinfo.objects.filter(id=x.author_id)[0].user_nickname
                if last_name:
                    last_name = last_name
                else:
                    last_name = 'null'
                tmp = {'last_time':last_time,'last_name':last_name}
                tmp_list.append(tmp)
            tmp_list.sort(key=operator.itemgetter('last_time'),reverse=True)


            datetime = floor_1_res[0].post_time
            content = floor_1_res[0].content
            watches = i.watches
            like_num = floor_1_res[0].like_num
            topped = i.topped
            stared = i.stared
            tag = i.tag
            floor_list = Floor.objects.filter(post_id=i.id)
            reply_num = 0
            for x in floor_list:
                reply_num = reply_num+1
            reply_num = reply_num-1
               
            content = {'id':str(i.id), 'title':i.title, 'author':author_name, 'nickname':nickname, 'teacher_identity':teacher_identity, 'datetime':str(datetime), 'content':content, 'read':str(watches), 'like':str(like_num), 'reply_num':reply_num ,'topped':topped ,'stared':stared, 'tag':tag, 'last_time':tmp_list[0]['last_time'], 'last_name':tmp_list[0]['last_name']}
            post_list.append(content)
        post_list.sort(key=operator.itemgetter('last_time'),reverse=True)
        #msg = "{\"msg\":\"ok\"" + "\"post_list\"" + "\""+ post_list+ "\"" +"}"\
        #res_dict = {'msg':'ok', 'post_list':post_list}
        return JsonResponse(post_list,safe=False)
    else:
        return JsonResponse([],safe=False)
        

#置顶帖子
def topPost(request):
    if(request.method!='POST'):
        return None
    dict = request.POST
    post_id = dict.get('postId')
    res = Post.objects.filter(id=post_id)
    if res:
        topped = Post.objects.filter(id=post_id).update(topped=1)
        msg = "ok"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2) 
    else:
        return HttpResponse('该帖子id不存在')


#取消置顶帖子
def cancelTopPost(request):
    if(request.method!='POST'):
        return None
    dict = request.POST
    post_id = dict.get('postId')
    res = Post.objects.filter(id=post_id)
    if res:
        topped = Post.objects.filter(id=post_id).update(topped=0)
        msg = "ok"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2) 
    else:
        return HttpResponse('该帖子id不存在')


#加精帖子
def starPost(request):
    if(request.method!='POST'):
        return None
    dict = request.POST
    post_id = dict.get('postId')
    res = Post.objects.filter(id=post_id)
    if res:
        topped = Post.objects.filter(id=post_id).update(stared=1)
        msg = "ok"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2) 
    else:
        return HttpResponse('该帖子id不存在')


#取消加精帖子
def cancelStarPost(request):
    if(request.method!='POST'):
        return None
    dict = request.POST
    post_id = dict.get('postId')
    res = Post.objects.filter(id=post_id)
    if res:
        topped = Post.objects.filter(id=post_id).update(stared=0)
        msg = "ok"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2) 
    else:
        return HttpResponse('该帖子id不存在')


#搜索课程（根据课程标题及简介模糊搜索）
def searchCourse(request):
    if(request.method!='POST'):
        return None
    dict = request.POST
    keyWord = dict.get('keyWord')
    res = Course.objects.filter(Q(course_name__contains=keyWord) | Q(course_intro__contains =keyWord))
    if res:
        course_list = []
        for i in res:
            course_id = str(i.id)
            course_name = i.course_name
            course_intro = i.course_intro
            if not course_intro:
                course_intro = 'null'
            start_time = str(i.start_time)
            if not start_time:
                start_time = 'null'
            end_time = str(i.end_time)
            if not end_time:
                end_time = 'null'
            profession = i.profession
            if not profession:
                profession = 'null'
            rule = i.rule
            if not rule:
                rule = 'null'
            teacher_id = i.teacher_id_id
            if not teacher_id:
                teacher_name='null'
            else:
                teacher_name = Userinfo.objects.filter(id=teacher_id)[0].realname
            content = {'id':course_id, 'course_name':course_name, 'course_intro':course_intro, 'start_time':start_time, 'end_time':end_time, 'profession':profession, 'rule':rule, 'teacher_name':teacher_name}
            course_list.append(content)
        return JsonResponse(course_list,safe=False)
    else:
        return JsonResponse([],safe=False)


#搜索帖子（根据帖子标题搜索）
def searchPost(request):   
    if(request.method!='POST'):
        return None
    dict = request.POST
    keyWord = dict.get('keyWord')
    forumId = dict.get('forumId')
    res = Post.objects.filter(Q(title__contains=keyWord) & Q(course_id=forumId))
    if res:
        post_list = []
        for i in res:
            author_name = Userinfo.objects.filter(id=i.owner_id)[0].username
            nickname = Userinfo.objects.filter(id=i.owner_id)[0].user_nickname
            if nickname:
                nickname = nickname
            else:
                nickname = 'null'
            teacher_identity = Userinfo.objects.filter(id=i.owner_id)[0].teacher_identity
            if teacher_identity:
                teacher_identity = str(teacher_identity)
            else:
                teacher_identity = 'null'
            floor_1_res = Floor.objects.filter(Q(post_id=i.id) & Q(floor_num =1))


            floor_res = Floor.objects.filter(post_id=i.id)
            tmp_list = []
            for x in floor_res:
                last_time = str(x.post_time)
                last_name = Userinfo.objects.filter(id=x.author_id)[0].user_nickname
                if last_name:
                    last_name = last_name
                else:
                    last_name = 'null'
                tmp = {'last_time':last_time,'last_name':last_name}
                tmp_list.append(tmp)
            tmp_list.sort(key=operator.itemgetter('last_time'),reverse=True)


            datetime = floor_1_res[0].post_time
            content = floor_1_res[0].content
            watches = i.watches
            like_num = floor_1_res[0].like_num
            topped = i.topped
            stared = i.stared
            tag = i.tag
            floor_list = Floor.objects.filter(post_id=i.id)
            reply_num = 0
            for x in floor_list:
                reply_num = reply_num+1
            reply_num = reply_num-1
               
            content = {'id':str(i.id), 'title':i.title, 'author':author_name, 'nickname':nickname, 'teacher_identity':teacher_identity, 'datetime':str(datetime), 'content':content, 'read':str(watches), 'like':str(like_num), 'reply_num':reply_num ,'topped':topped ,'stared':stared,'tag':tag,'last_time':tmp_list[0]['last_time'], 'last_name':tmp_list[0]['last_name']}
            post_list.append(content)
        post_list.sort(key=operator.itemgetter('last_time'),reverse=True)
        #msg = "{\"msg\":\"ok\"" + "\"post_list\"" + "\""+ post_list+ "\"" +"}"\
        #res_dict = {'msg':'ok', 'post_list':post_list}
        return JsonResponse(post_list,safe=False)
    else:
        return JsonResponse([],safe=False)


#删除帖子
def deletePost(request):   
    if(request.method!='POST'):
        return None
    dict = request.POST
    postId = dict.get('postId')
    try:
        floor = Floor.objects.filter(post_id=postId).delete()
        post = Post.objects.filter(id=postId).delete()
        msg = "ok"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2) 
    except Exception:
        res = 'api_ct deletePost error'
        return HttpResponse(res)

url_ct = [
	#url('getPostInfo',getPostInfo),
    url('replyPost',replyPost),
    url('cicleAllPost',cicleAllPost),
    url('topPost',topPost),
    url('starPost',starPost),
    url('cancelTopPost',cancelTopPost),
    url('cancelStarPost',cancelStarPost),
    url('searchPost',searchPost),
    url('searchCourse',searchCourse),
    url('deletePost',deletePost),
	]