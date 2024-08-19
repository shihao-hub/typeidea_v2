from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from blog.models import Category, Tag, Post


def index_view(request):
    pass


def _common_get_list(request):
    pass


def category_list_view(request, id_var):
    pass


def tag_list_view(request, id_var):
    pass


def post_list_view(request: WSGIRequest):
    print(f"post_list_view:")
    if request.method == "GET":
        res = Post.get_queryset_mixin()
        print(f"res: {res}")
        return HttpResponse(content=b"get_post_list_view")
    else:
        raise Exception()


def post_detail_view(request: WSGIRequest, id_var):
    print(f"post_detail_view:")
    if request.method == "GET":
        res = Post.get_queryset_mixin(dict(id=id_var))
        print(f"res: {res}")
        return HttpResponse(content=b"get_post_list_view")
    else:
        raise Exception()
