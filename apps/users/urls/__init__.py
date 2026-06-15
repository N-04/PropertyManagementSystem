# 文件说明：声明 Python 包，便于模块被项目导入。

from django.urls import path, include
from .menu_urls import urlpatterns as menu_urlpatterns

urlpatterns = [

    path(
        'menu/',
        include('apps.users.urls.menu_urls')
    ),

]