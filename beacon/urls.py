"""beacon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from fire import views
from fire import api_ztw
from fire import api_jyh
from fire import api_zzc
from fire import api_ct

urlpatterns = [
    url(r'^admin/', admin.site.urls),    
    
    url(r'^test_add/', views.test_add),
    url(r'^test_find/', views.test_find),

]
urlpatterns += api_ztw.url_ztw

urlpatterns += api_jyh.url_jyh
urlpatterns += api_zzc.url_zzc
urlpatterns += api_ct.url_ct

