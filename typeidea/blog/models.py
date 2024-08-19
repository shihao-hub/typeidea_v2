import collections
import uuid

from django.contrib.auth.models import User
from django.db import models

from shared.model_mixin import CommonModelMixin

const = collections.namedtuple(f"const_{str(uuid.uuid4()).replace('-', '')}", [
    "owner_name"
])(**dict(
    owner_name="作者"
))


# -------------------------------------------------------------------------------------------------------------------- #
class Category(CommonModelMixin, models.Model):
    STATUS_NORMAL, STATUS_DELETE = 1, 0
    STATUS_ITEMS = ((STATUS_NORMAL, "正常"), (STATUS_DELETE, "删除"))

    name = models.CharField("名称", max_length=50)
    status = models.PositiveIntegerField("状态", default=STATUS_NORMAL, choices=STATUS_ITEMS)
    is_nav = models.BooleanField("是否为导航", default=False)
    created_time = models.DateTimeField("创建时间", auto_now_add=True)

    owner = models.ForeignKey(User, verbose_name=const.owner_name, on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = "文章分类"

    def __str__(self):
        return self.name


class Tag(CommonModelMixin, models.Model):
    STATUS_NORMAL, STATUS_DELETE = 1, 0
    STATUS_ITEMS = ((STATUS_NORMAL, "正常"), (STATUS_DELETE, "删除"))

    name = models.CharField("名称", max_length=50)
    status = models.PositiveIntegerField("状态", default=STATUS_NORMAL, choices=STATUS_ITEMS)
    created_time = models.DateTimeField("创建时间", auto_now_add=True)

    owner = models.ForeignKey(User, verbose_name=const.owner_name, on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = "文章标签"

    def __str__(self):
        return self.name


# -------------------------------------------------------------------------------------------------------------------- #
class Post(CommonModelMixin, models.Model):
    STATUS_NORMAL, STATUS_DELETE, STATUS_DRAFT = 1, 0, 2
    STATUS_ITEMS = ((STATUS_NORMAL, "正常"), (STATUS_DELETE, "删除"), (STATUS_DRAFT, "草稿"))

    title = models.CharField("标题", max_length=255)
    description = models.CharField("摘要", max_length=1024, blank=True)
    content = models.TextField("正文", help_text="正文必须为 MarkDown 格式")
    status = models.PositiveIntegerField("状态", default=STATUS_NORMAL, choices=STATUS_ITEMS)
    created_time = models.DateTimeField("创建时间", auto_now_add=True)
    # updated_time = models.DateTimeField("更新时间")

    # (N)!: 当尝试删除一个被外键引用的对象（此处指 Category）时，Django 会引发一个 ProtectedError，从而阻止该对象被删除
    # (N)!: 使用 PROTECT 可以帮助你在设计数据库模型时维护数据完整性，确保不会意外删除仍在使用的对象。
    category = models.ForeignKey(Category, verbose_name=Category._meta.verbose_name, on_delete=models.PROTECT)
    owner = models.ForeignKey(User, verbose_name=const.owner_name, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name=Tag._meta.verbose_name)

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.title} - {self.owner}"
