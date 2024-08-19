import django.http
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from blog.adminforms import PostAdminForm
from blog.models import Category, Tag, Post
from shared.modeladmin_mixin import SetOwnerToCurrentUserMixin
from typeidea.custom_site import custom_admin_site


class CategoryOwnerFilterForPostAdmin(admin.SimpleListFilter):
    """ 顾名思义，过滤文章作者，登录用户只能看到自己创建的文章 """
    title = "分类过滤器"
    parameter_name = "owner_category"  # (N)!: 查询时 url 参数的名字，比如 id=1 时，URL 后面的 Query 部分是 ?owner_category=1

    def lookups(self, request, model_admin):
        # print("CategoryOwnerFilterForPostAdmin-lookups:")
        # print(f"request type: {type(request)}") # 'django.core.handlers.wsgi.WSGIRequest'
        # (N)!: 此处就是将作者过滤成当前用户，又要注意的是此处的返回值就是管理页过滤器显示的内容
        return Category.get_queryset_mixin(dict(owner=request.user)).values_list("id", "name")

    def queryset(self, request, queryset):
        print("CategoryOwnerFilterForPostAdmin-queryset:")
        category_id = self.value()
        print(f"category_id: {category_id}")
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


class PostInline(admin.TabularInline):
    """ 产品经理说：我们需要在分类页面直接编辑文章 """
    # (Q)!: 跑一下发现，此处就是生成一个要创建 Post 的表单（不是弹窗表单）
    fields = ("title", "description",)
    extra = 1
    model = Post


# -------------------------------------------------------------------------------------------------------------------- #
@admin.register(Category, site=custom_admin_site)
class CategoryAdmin(SetOwnerToCurrentUserMixin, admin.ModelAdmin):
    inlines = (PostInline,)
    # (N)!: list_display 是一个元组或列表，用于定义在模型的列表页面中显示哪些字段
    #       它用于控制在模型的列表视图中，表格的列显示哪些字段。这个视图通常是你在 Django Admin 中看到的对象列表。
    list_display = ("name", "status", "is_nav", "owner", "created_time",)
    list_filter = ("name",)
    # (N)!: fields 是一个元组或列表，用于定义在模型的表单页面中显示哪些字段
    #       它用于控制在模型的编辑页面中，表单中显示哪些字段。这个视图是你在 Django Admin 中编辑对象时看到的。
    fields = ("name", "status", "is_nav",)

    def save_model(self, *args, **kwargs):
        """ 这部分代码重复又该如何抽取出去呢？ """
        return self.save_model_mixin(*args, **kwargs)


@admin.register(Tag, site=custom_admin_site)
class TagAdmin(SetOwnerToCurrentUserMixin, admin.ModelAdmin):
    list_display = ("name", "status", "created_time",)
    fields = ("name", "status",)

    def save_model(self, *args, **kwargs):
        return self.save_model_mixin(*args, **kwargs)


@admin.register(Post, site=custom_admin_site)
class PostAdmin(SetOwnerToCurrentUserMixin, admin.ModelAdmin):
    form = PostAdminForm  # (Q)!: 此处的作用应该是接受其他地方发来的数据然后存储？
    list_display = ("title", "status", "category", "show_tags", "custom_operator", "owner", "created_time",)
    list_display_links = ()
    # (N)!: 此处的结构就是编辑页面的表单展示的结构
    # fields = (
    #     ("category", "title"),
    #     "description", "status", "content", "tags"
    # )
    # (N)!: fieldsets 比 fields 更灵活
    fieldsets = (
        ("基础配置", {
            "description": "基础配置描述",
            "fields": (
                ("title", "category"),
                "status"
            )
        }),
        ("内容", {
            "fields": (
                "description",
                "content"
            )
        }),
        ("额外信息", {
            # "classes": ("collapse",),
            "fields": ("tags",)
        })
    )
    # (N)!: 控制多对多字段的展示效果（运行一下查看效果）
    filter_horizontal = ("tags",)
    # filter_vertical = ("tags",)
    # list_filter = ("category",)  # (N)!: 给管理页添加了过滤器，存在需要注意的地方是列表页应该只能显示当前登录的用户创建的文章
    list_filter = (CategoryOwnerFilterForPostAdmin,)
    search_fields = ("title", "category__name",)  # (N)!: 给管理页添加了搜索框
    actions_on_top = True

    # actions_on_bottom = True
    # save_on_top = True

    def custom_operator(self, obj):
        return format_html("<a href='{}'>编辑</a>", reverse("custom_admin:blog_post_change", args=(obj.id,)))

    custom_operator.short_description = "操作"

    def show_tags(self, obj):
        return ", ".join(obj.tags.all().values_list("name", flat=True))

    show_tags.short_description = "标签"

    def save_model(self, *args, **kwargs):
        return self.save_model_mixin(*args, **kwargs)

    def get_queryset(self, request):
        """ (td)!: 注意，其他 admin 也需要添加这个...（列表页展示的时候，应该只显示当前用户创建的数据） """
        res = super(PostAdmin, self).get_queryset(request)
        return res.filter(owner=request.user)
