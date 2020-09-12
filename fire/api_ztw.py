from django.http.response import HttpResponse
from django.forms.models import model_to_dict
from django.conf.urls import url
from fire.models import *
import traceback
import datetime
def json_raw(dict):
	return str(dict).replace('\'','\"').replace('None','null')
def model_to_dict_fixed(model):
	d = model_to_dict(model)
	for key in d.keys():
		if d[key].__class__==datetime.datetime:
			d[key] = str(d[key])
	return d
def api_format(request):
	try:
		dict = request.POST
		msg = {}
		
		
	except:
		traceback.print_exc()
		msg['result']='Unexpected Error'
		return HttpResponse(json_raw(msg))
def addUser(request):
	try:
		dict = request.POST
		msg = {}
		
		tag = Userinfo()
		tag.username = dict.get('username',None)
		tag.user_password = dict.get('user_password',None)
		tag.user_nickname = dict.get('user_nickname',None)
		tag.introduction = dict.get('introduction',None)
		tag.phonenumber = dict.get('phonenumber',None)
		tag.email = dict.get('email',None)
		tag.qq = dict.get('qq',None)
		tag.teacher_identity = dict.get('teacher_identity',None)
		tag.school = dict.get('school',None)
		tag.school_id = dict.get('school_id',None)
		tag.realname = dict.get('realname',None)
		tag.profession = dict.get('profession',None)		
		if tag.username == None or tag.user_password == None:
			msg['result'] = '用户名或密码不能为空。'
			return HttpResponse(json_raw(msg))
		elif Userinfo.objects.filter(username=tag.username):
			msg['result'] = '该用户名已被注册。'
			return HttpResponse(json_raw(msg))
			
		msg['result']='OK'
		tag.save()
		return HttpResponse(json_raw(msg))
	except:
		traceback.print_exc()
		msg['result']='Unexpected Error'
		return HttpResponse(json_raw(msg))
def setCourseRule(request):
	try:
		msg = {}
		dict = request.POST
		print(dict	)
		
		id = dict.get('id',None)
		if id == None:
			msg['result']='课程id不能为空。'
			return HttpResponse(json_raw(msg))
		
		course = Course.objects.filter(id=id).first()
		
		course.rule = dict.get('rule',None)
		if course.rule == None:
			msg['result']='课程规则不能为空。'
			return HttpResponse(json_raw(msg))
		course.save()
		msg['result']='OK'
		return HttpResponse(json_raw(msg))

		
		
	except:
		traceback.print_exc()
		msg['result']='Unexpected Error'
		return HttpResponse(json_raw(msg))
def login(request):
	try:
		dict = request.POST
		msg = {}
		username = dict.get('username',None)
		user_password = dict.get('user_password',None)
		if username==None or user_password==None:
			msg['result']='用户名或密码不能为空。'
			return HttpResponse(json_raw(msg))
		
		qset = Userinfo.objects.filter(username=username,user_password=user_password)
		if qset:
			msg.update(model_to_dict(qset.first()))
			msg['result']='OK'
			return HttpResponse(json_raw(msg))
		else:
			msg['result']='用户不存在或密码错误。'
			return HttpResponse(json_raw(msg))
		
	except:
		traceback.print_exc()
		msg['result']='Unexpected Error'
		return HttpResponse(json_raw(msg))
def courseQuery(request):
	try:
		dict = request.POST
		msg = {}
		
		qset = Course.objects.all()
		courses=[]
		for q in qset:
			courses.append(model_to_dict_fixed(q))
		msg['courses']=courses
		return HttpResponse(json_raw(msg))
		
	except:
		traceback.print_exc()
		msg['result']='Unexpected Error'
		return HttpResponse(json_raw(msg))
def createPost(request):
	try:
		msg={}
		dict = request.POST
		
		tag = Post()
		tag.title = dict.get('title',None)
		
		course = dict.get('course',None)
		tag_courses = Course.objects.filter(id=course)		
		if tag_courses:
			tag.course = tag_courses.first()
		else:
			msg['result']='该课程id不存在。'
			return HttpResponse(json_raw(msg))
		
		owner = dict.get('owner',None)
		tag_owners = Userinfo.objects.filter(id=owner)
		if tag_owners:
			tag.owner = tag_owners.first()
		else:
			msg['result']='该帖子所有者id不存在。'
			return HttpResponse(json_raw(msg))
		
		tag.watches = 0
		tag.tag = dict.get('tag',None)			
		
		if tag.title==None:
			msg['result']='标题不能为空。'
			return HttpResponse(json_raw(msg))
		elif tag.course==None:
			msg['result']='所属课程不能为空。'
			return HttpResponse(json_raw(msg))
		elif tag.title==None:
			msg['owner']='帖子所有者不能为空。'
			return HttpResponse(json_raw(msg))
		tag.save()
		
		floor = Floor()
		floor.author = tag.owner
		floor.post = tag
		floor.content = dict.get('content',None)
		floor.post_time = datetime.datetime.now()
		floor.floor_num = 1
		floor.reply_floor = 0
		floor.like_num = 0		
		floor.save()
		

		
		msg['id']=tag.id
		msg['result']='帖子创建成功'
		return HttpResponse(json_raw(msg))
		
		
	except:
		traceback.print_exc()
		msg['result']='Unexpected Error'
		return HttpResponse(json_raw(msg))
def postQuery(request):
	try:
		dict = request.POST
		msg = {}
		floors = []
		id = dict.get('id',None)
		if id==None:
			msg['result']='帖子id不能为空。'
			return HttpResponse(json_raw(msg))
		post = Post.objects.get(id=id)
		print(post.title,post.id)
		qset = Floor.objects.filter(post=post)
		if not qset:
			msg['result']='该帖子没有楼层，请联系后台。'
			return HttpResponse(json_raw(msg))
		for q in qset:
			floors.append(model_to_dict_fixed(q))
		msg['floors']=floors
		msg['result']='OK'
		return HttpResponse(json_raw(msg))
		
		
	except:
		traceback.print_exc()
		msg['result']='Unexpected Error'
		return HttpResponse(json_raw(msg))	
	
	
	

url_ztw = [
	url('addUser',addUser),
	url('setCourseRule',setCourseRule),
	url('login',login),
	url('courseQuery',courseQuery),
	url('createPost',createPost),
	url('postQuery',postQuery)
	]
