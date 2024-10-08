"""typeidea URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin

from typeidea.custom_site import custom_admin_site

urlpatterns = [
    url(r"^blog/", include(("blog.urls", "blog"), namespace="blog")),

    url(r'^superadmin/', admin.site.urls),  # 用户模块的管理（管理用户）
    url(r'^admin/', custom_admin_site.urls),  # 文章分类等数据的管理（管理业务）
]
