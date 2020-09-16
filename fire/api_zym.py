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

def get_applications_by_course_id(request):
	try:
		dict = request.GET
		msg = {}
		msg['message'] = ''
		courseid = dict.get('course_id', None)
		if courseid == None:
			msg['message'] = '课程id不能为空。'
			return JsonResponse(msg, safe=False)

		list = CourseApplication.objects.filter(course=courseid)
		unhandled = []
		accepted = []
		rejected = []
		if list:
			for i in list:
				app = model_to_dict(i)
				type = app.get('result', None)
				if type:
					if type == 0:
						unhandled.append(app)
					elif type == 1:
						accepted.append(app)
					elif type == 2:
						rejected.append(app)
					else:
						msg['message'] = '未知类型的申请结果。'
						return JsonResponse(msg, safe=False)
			msg['unhandled_applications'] = unhandled
			msg['accepted_applications'] = accepted
			msg['rejected_applications'] = rejected
			msg['message'] = 'OK'
			return JsonResponse(msg, safe=False)
		else:
			msg['message'] = '课程不存在。'
			return JsonResponse(msg, safe=False)
	except:
		traceback.print_exc()
		msg['message'] = 'Unexpected Error'
		return JsonResponse(msg, safe=False)

def accept_application(request):
	try:
		dict = request.GET
		msg = {}
		msg['message'] = ''
		id = dict.get('course_application_id', None)
		if id == None:
			msg['message'] = '申请id不能为空。'
			return JsonResponse(msg, safe=False)
		app = CourseApplication.objects.filter(id=id)
		if app:
			app.update(result=1)
			ap = app.first()
			new = UserCourse()
			new.user = ap.user
			new.course = ap.course
			new.save()
			msg['message'] = 'OK'
			return JsonResponse(msg, safe=False)
		else:
			msg['message'] = '申请记录不存在。'
			return JsonResponse(msg, safe=False)
	except:
		traceback.print_exc()
		msg['message'] = 'Unexpected Error'
		return JsonResponse(msg, safe=False)

def reject_application(request):
	try:
		dict = request.GET
		msg = {}
		msg['message'] = ''
		id = dict.get('course_application_id', None)
		if id == None:
			msg['message'] = '申请id不能为空。'
			return JsonResponse(msg, safe=False)
		app = CourseApplication.objects.filter(id=id)
		if app:
			app.update(result=2)
			msg['message'] = 'OK'
			return JsonResponse(msg, safe=False)
		else:
			msg['message'] = '申请记录不存在。'
			return JsonResponse(msg, safe=False)
	except:
		traceback.print_exc()
		msg['message'] = 'Unexpected Error'
		return JsonResponse(msg, safe=False)

def quit_course(request):
	try:
		dict = request.GET
		msg = {}
		msg['message'] = ''
		userid = dict.get('user_id', None)
		courseid = dict.get('course_id', None)
		if userid == None:
			msg['message'] = '用户id不能为空。'
			return JsonResponse(msg, safe=False)
		if courseid == None:
			msg['message'] = '课程id不能为空。'
			return JsonResponse(msg, safe=False)
		record = UserCourse.objects.filter(user=userid, course=courseid).first()
		if record:
			record_dict = model_to_dict(record)
			identity = record_dict.get('user_identity', None)
			msg['record'] = record_dict
			if identity == 0:
				record.delete()
				msg['message'] = 'OK'
				return JsonResponse(msg, safe=False)
			elif identity == 1:
				msg['message'] = '用户属于管理员身份，无法退出课程。'
				return JsonResponse(msg, safe=False)
			else:
				msg['message'] = '未知的用户身份。'
				return JsonResponse(msg, safe=False)
		else:
			msg['message'] = '该用户尚未参加改课程。'
			return JsonResponse(msg, safe=False)
	except:
		traceback.print_exc()
		msg['message'] = 'Unexpected Error'
		return JsonResponse(msg, safe=False)

def quit_delete(request):
	try:
		dict = request.GET
		msg = {}
		msg['message'] = ''
		courseid = dict.get('course_id', None)
		if courseid == None:
			msg['message'] = '课程id不能为空。'
			return JsonResponse(msg, safe=False)
		course = Course.objects.filter(id=courseid).first()
		if course:
			course.delete()
			msg['message'] = 'OK'
			return JsonResponse(msg, safe=False)
		else:
			msg['message'] = '待删除的课程不存在。'
			return JsonResponse(msg, safe=False)
	except:
		traceback.print_exc()
		msg['message'] = 'Unexpected Error'
		return JsonResponse(msg, safe=False)

def get_courses_in_possession(request):
	try:
		dict = request.GET
		msg = {}
		msg['message'] = ''
		userid = dict.get('user_id', None)
		if userid == None:
			msg['message'] = '用户id不能为空。'
			return JsonResponse(msg, safe=False)

		list = Course.objects.filter(teacher_id=userid)
		course_list = []
		if list:
			for i in list:
				c = model_to_dict(i)
				course_list.append(c)
			msg['course_list'] = course_list
			msg['message'] = 'OK'
			return JsonResponse(msg, safe=False)
		else:
			msg['message'] = '该用户未创建任何课程。'
			return JsonResponse(msg, safe=False)
	except:
		traceback.print_exc()
		msg['message'] = 'Unexpected Error'
		return JsonResponse(msg, safe=False)

url_zym = [
	url('usercourse', get_course_by_userid),
	url('userdetail', get_userinfo_by_userid),
	url('class/application/getall', get_applications_by_course_id),
	url('class/application/accept', accept_application),
	url('class/application/reject', reject_application),
	url('class/quit', quit_course),
	url('class/delete', quit_delete),
	url('class/asowner', get_courses_in_possession),
	]
