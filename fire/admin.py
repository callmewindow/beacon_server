from django.contrib import admin
from fire import models

admin.site.register(models.Course)
admin.site.register(models.Floor)
admin.site.register(models.Post)
admin.site.register(models.UserCourse)
admin.site.register(models.UserPlayRecords)
admin.site.register(models.UserVideo)
admin.site.register(models.Userinfo)
admin.site.register(models.Videos)
admin.site.register(models.LikeRecord)
admin.site.register(models.CourseApplication)
admin.site.register(models.FriendApplication)
admin.site.register(models.FriendRecord)
admin.site.register(models.SystemMessage)
admin.site.register(models.PrivateMessage)
# Register your models here.
