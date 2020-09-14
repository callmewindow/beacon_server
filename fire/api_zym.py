from django.http.response import HttpResponse
from django.forms.models import model_to_dict
from django.conf.urls import url
from fire.models import *
from django.http import JsonResponse
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
		msg['message']='Unexpected Error'
		return JsonResponse(msg, safe=False)

def get_course_by_userid(request):
	try:
		dict = request.GET
		msg = {}
		msg['message'] = 'OK'
		userid = dict.get('userid', None)
		if userid == None:
			msg['message'] = '用户id不能为空。'
			return JsonResponse(msg, safe=False)

		courses = []
		result = UserCourse.objects.filter(user=userid)
		if len(result) == 0:
			msg['message'] = '该用户未参加任何课程。'
			return JsonResponse(msg, safe=False)
		for i in result:
			model = model_to_dict_fixed(i)
			course_model = Course.objects.filter(id=model['course'])
			if len(course_model) is 0:
				msg['message'] = '未找到课程。'
				return JsonResponse(msg, safe=False)
			else:
				course_dict = model_to_dict(course_model.first())
				course_name = course_dict.get('course_name', None)
				course_intro = course_dict.get('course_intro', None)
				start_time = course_dict.get('start_time', None)
				profession = course_dict.get('profession', None)
				teachername = course_dict.get('teacher_name', None)
				studentnum = UserCourse.objects.filter(course=model['course']).count()
				course = {
					"course_name": course_name,
					"course_intro": course_intro,
					"start_time": start_time,
					"profession": profession,
					"studentnum": studentnum,
					"teachername": teachername
				}
				courses.append(course)

		msg['courses'] = courses
		return JsonResponse(msg, safe=False)
	except:
		traceback.print_exc()
		msg['message'] = 'Unexpected Error'
		return JsonResponse(msg, safe=False)

def get_userinfo_by_userid(request):
	try:
		dict = request.GET
		msg = {}
		msg['message'] = ''
		userid = dict.get('userid', None)
		if userid == None:
			msg['message'] = '用户id不能为空。'
			return JsonResponse(msg, safe=False)

		userinfo = Userinfo.objects.filter(id=userid).first()
		if userinfo:
			user_dict = model_to_dict(userinfo)
			course_time = 0
			course_point_together = 0
			records = UserCourse.objects.filter(user=userid)
			course_num = len(records)
			for r in records:
				record_dict = model_to_dict(r)
				time = record_dict.get('watch_duration', None)
				if time:
					course_time += time
				point = record_dict.get('point', None)
				if point:
					course_point_together += point
			user = {
				"username": user_dict.get('username', None),
				"teacher identity": user_dict.get('teacher_identity', None),
				"school": user_dict.get('school', None),
				"profession": user_dict.get('profession', None),
				"course number": course_num,
				"school id": user_dict.get('school_id', None),
				"coursetime": course_time,
				"score": course_point_together,
				"nickname": user_dict.get('user_nickname', None),
				"introduction": user_dict.get('introduction', None),
				"password": user_dict.get('user_password', None),
				"phonenum": user_dict.get('phonenumber', None),
				"email": user_dict.get('email', None),
				"realname": user_dict.get('realname', None),
			}
			msg['message'] = 'OK'
			msg['user'] = user
			return JsonResponse(msg, safe=False)
		else:
			msg['message'] = '用户不存在。'
			return JsonResponse(msg, safe=False)


	except:
		traceback.print_exc()
		msg['message'] = 'Unexpected Error'
		return JsonResponse(msg, safe=False)

url_zym = [
	url('usercourse',get_course_by_userid),
	url('userdetail',get_userinfo_by_userid),
	]
