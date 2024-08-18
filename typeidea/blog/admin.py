from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from blog.models import Category, Tag, Post
from shared.modeladmin_mixin import SetOwnerToCurrentUserMixin


@admin.register(Category)
class CategoryAdmin(SetOwnerToCurrentUserMixin, admin.ModelAdmin):
    # (N)!: list_display 是一个元组或列表，用于定义在模型的列表页面中显示哪些字段
    #       它用于控制在模型的列表视图中，表格的列显示哪些字段。这个视图通常是你在 Django Admin 中看到的对象列表。
    list_display = ("name", "status", "is_nav", "created_time",)

    # (N)!: fields 是一个元组或列表，用于定义在模型的表单页面中显示哪些字段
    #       它用于控制在模型的编辑页面中，表单中显示哪些字段。这个视图是你在 Django Admin 中编辑对象时看到的。
    fields = ("name", "status", "is_nav",)

    def save_model(self, *args, **kwargs):
        """ 这部分代码重复又该如何抽取出去呢？ """
        return self.save_model_mixin(*args, **kwargs)


@admin.register(Tag)
class TagAdmin(SetOwnerToCurrentUserMixin, admin.ModelAdmin):
    list_display = ("name", "status", "created_time",)
    fields = ("name", "status",)

    def save_model(self, *args, **kwargs):
        return self.save_model_mixin(*args, **kwargs)


@admin.register(Post)
class PostAdmin(SetOwnerToCurrentUserMixin, admin.ModelAdmin):
    list_display = ("title", "status", "created_time", "category", "custom_operator",)
    list_display_links = ()
    # (N)!: 此处的结构就是编辑页面的表单展示的结构
    fields = (
        ("category", "title"),
        "description", "status", "content", "tags"
    )
    list_filter = ("category",)
    search_fields = ("title", "category__name",)
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True

    def custom_operator(self, obj):
        return format_html("<a href='{}'>编辑</a>", reverse("admin:blog_post_change", args=(obj.id,)))

    custom_operator.short_description = "操作"

    def save_model(self, *args, **kwargs):
        return self.save_model_mixin(*args, **kwargs)
