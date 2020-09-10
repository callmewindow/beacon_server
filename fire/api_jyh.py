from django.http import HttpResponse
import pymysql

def getVideo(request):
    if(request.method != 'GET'): 
        msg = '需要GET请求'
        res = '{"message":' + msg +'}'
        return HttpResponse(res)
    
    class_id = request.GET.get("class_id", -1)
    if(class_id == -1):
        msg = '需要课程id'
        res = '{"message":' + msg +'}'
        return HttpResponse(res)

    # 实际环境中应该是localhost
    db = pymysql.connect("101.200.219.50", "fire", "Beacon123!")

    cursor = db.cursor()

    sql = '''
        select * from videos
    '''

    '''
        insert into videos(title, introduction, video_duration, local_address, course_id) values('先辈', '114514', now(), 'www.baidu.com', 114514);
    '''

    try:
        cursor.execute(sql)
    except Exception as e:
        print(e)

    db.close()

