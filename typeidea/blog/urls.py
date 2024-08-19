from django.conf.urls import url

import blog.views as views

urlpatterns = [
    url(r'^$', views.post_list_view, name="post_list_view"),
]
