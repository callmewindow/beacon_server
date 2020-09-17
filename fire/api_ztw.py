from django.http.response import HttpResponse
from django.forms.models import model_to_dict
from django.conf.urls import url
from fire.models import *
import traceback
import datetime
from dateutil.tz import gettz
def json_raw(dict):
	return str(dict).replace('\'','\"').replace('None','null')
def model_to_dict_fixed(model):
	d = model_to_dict(model)
	for key in d.keys():
		if d[key].__class__==datetime.datetime:
			d[key] = d[key].strftime('%Y-%m-%d %H:%M:%S')
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
		elif Userinfo.objects.filter(email=tag.email):
			msg['result'] = '该邮箱已被注册。'
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
		
		courses = Course.objects.all()
		msg_courses=[]
		for course in courses:
			course_dict = model_to_dict_fixed(course)
			
			teacher = course.teacher_id
			if not teacher:
				course_dict['teacher']=None
			else:
				course_dict['teacher']=model_to_dict_fixed(teacher)
			course_dict['student_number']=UserCourse.objects.filter(course=course).count()
			msg_courses.append(course_dict)
		msg['courses']=msg_courses
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
		tag.stared = False
		tag.topped = False
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
		now = datetime.datetime.now(tz=gettz('Asia/Beijing'))
		floor.post_time = now
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
		post.watches += 1
		post.save()
		msg['post']=model_to_dict_fixed(post)
		owner = {}
		owner['user_nickname']=post.owner.user_nickname
		owner['teacher_identity']=post.owner.teacher_identity
		msg['post']['owner']=owner
		qset = Floor.objects.filter(post=post)
		if not qset:
			msg['result']='该帖子没有楼层，请联系后台。'
			return HttpResponse(json_raw(msg))
		for q in qset:
			qdict = model_to_dict_fixed(q)
			owner = {}
			owner['user_nickname']=q.author.user_nickname
			owner['teacher_identity']=q.author.teacher_identity
			qdict['owner']=owner
			floors.append(qdict)
		msg['floors']=floors
		msg['result']='OK'
		return HttpResponse(json_raw(msg))
		
		
	except:
		traceback.print_exc()
		msg['result']='Unexpected Error'
		return HttpResponse(json_raw(msg))	
def getPoint(request):
	try:
		dict = request.POST
		msg = {}
		
		point = dict.get('point')
		if point == None:
			msg['result']='积分不能为空。'
			return HttpResponse(json_raw(msg))
		
		user_id = dict.get('user_id')
		if user_id == None:
			msg['result']='用户id不能为空。'
			return HttpResponse(json_raw(msg))
		course_id = dict.get('course_id')
		if course_id == None:
			msg['result']='课程id不能为空。'
			return HttpResponse(json_raw(msg))
		user = Userinfo.objects.filter(id=user_id)
		if not user:
			msg['result']='用户不存在。'
			return HttpResponse(json_raw(msg))
		course = Course.objects.filter(id=course_id)
		if not course:
			msg['result']='课程不存在。'
			return HttpResponse(json_raw(msg))
		
		
		user_course = UserCourse.objects.get(user=user,course=course)
		if not user_course:
			msg['result']='该用户未选择此课程。'
			return HttpResponse(json_raw(msg))
		user_course.point += int(point)
		
		if user_course.point<0:
			msg['result']='积分不足，无法扣除。'
			return HttpResponse(json_raw(msg))
		user_course.save()
		msg['result']='OK'
		return HttpResponse(json_raw(msg))
		
		
	except:
		traceback.print_exc()
		msg['result']='Unexpected Error'
		return HttpResponse(json_raw(msg))
def userCourse(request):
	try:
		dict = request.POST
		msg = {}
		
		user_id = dict.get('user_id')
		course_id = dict.get('course_id')
		if not user_id:
			msg['result']='用户id不能为空。'
			return HttpResponse(json_raw(msg))
		if not course_id:
			msg['result']='课程id不能为空。'
		users = Userinfo.objects.filter(id=user_id)
		courses = Course.objects.filter(id=course_id)
		if not users:
			msg['result']='该用户不存在。'
			return HttpResponse(json_raw(msg))
		if not courses:
			msg['result']='该课程不存在。'
			return HttpResponse(json_raw(msg))
		user = users.first()
		course = courses.first()
		
		user_courses = UserCourse.objects.filter(user=user,course=course)
		
		if not user_courses:
			msg['result']='该用户未选择此课程。'
			return HttpResponse(json_raw(msg))
		user_course = user_courses.first()
		
		videos = Videos.objects.filter(course=course)
		
		play_records = []
		msg_videos = []
		msg_user_videos = []
		for video in videos:
			msg_videos.append(model_to_dict_fixed(video))
			user_videos = UserVideo.objects.filter(user=user,video=video)
			if not user_videos:
				continue
			user_video = user_videos.first()
			msg_user_videos.append(model_to_dict(user_video))
			user_play_records = UserPlayRecords.objects.filter(user_video=user_video)
			for user_play_record in user_play_records:
				play_records.append(model_to_dict_fixed(user_play_record))
		
		
		msg['result']='OK'
		msg['user_course']=model_to_dict_fixed(user_course)
		msg['user_videos']=msg_user_videos
		msg['videos']=msg_videos
		msg['user_play_records']=play_records
		return HttpResponse(json_raw(msg))
		
	except:
		traceback.print_exc()
		msg['result']='Unexpected Error'
		return HttpResponse(json_raw(msg))
def getCourseWatches(request):
	try:
		dict = request.POST
		msg = {}
		
		id = dict.get('id')
		if not id:
			msg['result']='课程id不能为空。'
			return HttpResponse(json_raw(msg))
		courses = Course.objects.filter(id=id)
		if not courses:
			msg['result']='该课程不存在。'
			return HttpResponse(json_raw(msg))
		course = courses.first()
		videos = Videos.objects.filter(course=course)
		user_videos = []
		for video in videos:
			video_user_videos = UserVideo.objects.filter(video=video)
			for v in video_user_videos:
				user_videos.append(model_to_dict_fixed(v))
		msg['result']='OK'
		msg['user_videos']=user_videos
		return HttpResponse(json_raw(msg))
	except:
		traceback.print_exc()
		msg['result']='Unexpected Error'
		return HttpResponse(json_raw(msg))
def oneWatch(request):
	try:
		dict = request.POST
		msg = {}
		video_id = dict.get('video_id')
		user_id = dict.get('user_id')
		played_time = dict.get('played_time')
		start_play_time = dict.get('start_play_time')
		
		if (not video_id) or (not user_id) or (not played_time) or (not start_play_time):
			msg['result']='请求字段错误，请重试。'
			return HttpResponse(json_raw(msg))
		
		users = Userinfo.objects.filter(id=user_id)
		if not users:
			msg['result']='该用户不存在。'
			return HttpResponse(json_raw(msg))
		user = users.first()
		
		videos = Videos.objects.filter(id=video_id)
		if not videos:
			msg['result']='该视频不存在。'
			return HttpResponse(json_raw(msg))
		video = videos.first()
		
		course = video.course
		user_courses = UserCourse.objects.filter(course=course,user=user)
		if not user_courses:
			msg['result']='该用户未选该视频对应的课程。'
			return HttpResponse(json_raw(msg))
		#若游客或未选课学生观看视频，不计入课程的观看时长
		
		user_videos = UserVideo.objects.filter(user=user,video=video)
		user_video = None
		if not user_videos:
			user_video = UserVideo()
			user_video.user = user
			user_video.video = video
			user_video.video_viewed_time = 1
			user_video.video_viewed_times = int(played_time)
			user_video.save()
		else:
			user_video = user_videos.first()
			user_video.video_viewed_time += 1
			user_video.video_viewed_times += int(played_time)
			user_video.save()
		user_play_record = UserPlayRecords()
		user_play_record.user_video = user_video
		user_play_record.played_time = int(played_time)
		user_play_record.start_play_time = start_play_time
		user_play_record.save()
		

		user_course = user_courses.first()
		user_course.watch_duration += int(played_time)
		user_course.watch_num += 1
		user_course.save()
		msg['result']='OK'
		return HttpResponse(json_raw(msg))	
	except:
		traceback.print_exc()
		msg['result']='Unexpected Error'
		return HttpResponse(json_raw(msg))
def likeFloor(request):
	try:
		dict = request.POST
		msg = {}
		
		user_id = dict.get('user_id')
		floor_id = dict.get('floor_id')
		
		if not user_id:
			msg['result']='用户id不能为空。'
			return HttpResponse(json_raw(msg))
		if not floor_id:
			msg['result']='楼层id不能为空。'
			return HttpResponse(json_raw(msg))
		
		users = Userinfo.objects.filter(id=user_id)
		if not users:
			msg['result']='该用户不存在。'
			return HttpResponse(json_raw(msg))
		user = users.first()
		
		floors = Floor.objects.filter(id=floor_id)
		if not floors:
			msg['result']='该楼层不存在。'
			return HttpResponse(json_raw(msg))
		floor = floors.first()
		floor.like_num += 1
		floor.save()
		msg['result']='OK'
		return HttpResponse(json_raw(msg))
	except:
		traceback.print_exc()
		msg['result']='Unexpected Error'
		return HttpResponse(json_raw(msg))
def unlikeFloor(request):
	try:
		dict = request.POST
		msg = {}
		
		user_id = dict.get('user_id')
		floor_id = dict.get('floor_id')
		
		if not user_id:
			msg['result']='用户id不能为空。'
			return HttpResponse(json_raw(msg))
		if not floor_id:
			msg['result']='楼层id不能为空。'
			return HttpResponse(json_raw(msg))
		
		users = Userinfo.objects.filter(id=user_id)
		if not users:
			msg['result']='该用户不存在。'
			return HttpResponse(json_raw(msg))
		user = users.first()
		
		floors = Floor.objects.filter(id=floor_id)
		if not floors:
			msg['result']='该楼层不存在。'
			return HttpResponse(json_raw(msg))
		floor = floors.first()
		floor.like_num -= 1
		floor.save()
		msg['result']='OK'
		return HttpResponse(json_raw(msg))
		
	except:
		traceback.print_exc()
		msg['result']='Unexpected Error'
		return HttpResponse(json_raw(msg))
def hotCourses(request):
	try:
		dict = request.POST
		msg = {}
		msg_courses = []
		

		for course in Course.objects.all():
			msg_courses.append(model_to_dict_fixed(course))
		def counterFunc(course_dict):
			key = UserCourse.objects.filter(course=Course.objects.get(id=course_dict['id'])).count()
			course_dict['student_number']=key
			return key
		msg_courses.sort(key=counterFunc,reverse=True)
		if len(msg_courses)>10:
			msg_courses = msg_courses[0:10]
		msg['courses']=msg_courses
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
	url('postQuery',postQuery),
	url('getPoint',getPoint),
	url('userCourse',userCourse),
	url('getCourseWatches',getCourseWatches),
	url('oneWatch',oneWatch),
	url('^likeFloor$',likeFloor),
	url('unlikeFloor',unlikeFloor),
	url('hotCourses',hotCourses)
	]
