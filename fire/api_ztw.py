from django.http.response import HttpResponse
from django.conf.urls import url
from fire.modules import *

def add_user(request):
	dict = request.GET
	
	username = dict.get('username',None)
	password = dict.get('password',None)
	email = dict.get('email',None)
	user = UserInfo()
	user.username = dict.get('username',None)
	user.password = dict.get('password',None)
	user.save()
	
	
	print(dict)
	return HttpResponse('OK.')


url_ztw = [
	url('/addUser',add_user),
	
	]
