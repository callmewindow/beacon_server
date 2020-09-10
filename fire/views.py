from django.shortcuts import render
from fire.models import *
from django.http.response import HttpResponse
import random

def test_add(request):
    # 随机整数 作为学号
    for i in range(0, 5):
        username = int(random.uniform(0, 1) * 10000000000)
        # 从models文件中获取userinfo对象
        userinfo = Userinfo()
        # 给对象赋值
        userinfo.username = username
        userinfo.user_password = '123456'
        userinfo.user_nickname = 'zym' + str(i)
        # 插入数据
        userinfo.save()

    return HttpResponse('数据插入完毕')

def test_find(request):
    # django 也可以执行原生的sql语句
    #sql = 'select * from student'
    #result = Student.objects.raw(sql)

    # 查询name = tom1的数据
    result = Userinfo.objects.filter(user_nickname='zym1')
    """
    result为<class 'django.db.models.query.QuerySet'>的对象
    需要进行数据处理
    """
    arr = []
    for i in result:
        content = {'用户名': i.username, '密码': i.user_password, '昵称': i.user_nickname}
        arr.append(content)
    print(arr)
    print(type(arr))
    return HttpResponse(arr)
