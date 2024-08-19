from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from blog.models import Category, Tag, Post


def index_view(request):
    pass


def post_list_view(request: WSGIRequest, category_id=None, tag_id=None):
    print(f"post_list_view:")

    if not request.method == "GET":
        raise Exception(f"非法的请求 {request.method}")

    template_name = "blog/list.html"
    res = Post.get_queryset_mixin()
    print(f"res: {res}")
    return render(request, template_name, dict(
        name="post_list"
    ))


def post_detail_view(request: WSGIRequest, post_id):
    print(f"post_detail_view:")

    if not request.method == "GET":
        raise Exception(f"非法的请求 {request.method}")

    template_name = ""
    res = Post.get_queryset_mixin(dict(id=post_id))
    print(f"res: {res}")
    return render(request, template_name, dict(
        name="post_detail"
    ))
