import collections
import uuid

from django.contrib.auth.models import User
from django.db import models

from shared.model_mixin import CommonModelMixin

const = collections.namedtuple(f"const_{str(uuid.uuid4()).replace('-', '')}", [
    "owner_name"
])(**dict(
    owner_name="作者",
))


# -------------------------------------------------------------------------------------------------------------------- #
class Link(CommonModelMixin, models.Model):
    STATUS_NORMAL, STATUS_DELETE = 1, 0
    STATUS_ITEMS = ((STATUS_NORMAL, "正常"), (STATUS_DELETE, "删除"))

    title = models.CharField("标题", max_length=50)
    href = models.URLField("链接")  # (N)!: 默认长度为 200
    status = models.PositiveIntegerField("状态", default=STATUS_NORMAL, choices=STATUS_ITEMS)
    weight = models.PositiveIntegerField("权重", default=1, choices=zip(range(1, 6), range(1, 6)),
                                         help_text="权重高展示顺序靠前")
    created_time = models.DateTimeField("创建时间", auto_now_add=True)

    owner = models.ForeignKey(User, verbose_name=const.owner_name, on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = "友链"


class SiderBar(CommonModelMixin, models.Model):
    STATUS_SHOW, STATUS_HIDE = 1, 0
    STATUS_ITEMS = ((STATUS_HIDE, "隐藏"), (STATUS_SHOW, "展示"))
    SIDE_TYPE = zip(range(1, 5), ["HTML", "最热文章", "最新文章", "最近评论"])

    title = models.CharField("标题", max_length=50)
    display_type = models.PositiveIntegerField("展示类型", default=1, choices=SIDE_TYPE)
    content = models.CharField("", max_length=500, blank=True, help_text="如果设置的不是 HTML 类型，可为空")
    status = models.PositiveIntegerField("状态", default=STATUS_SHOW, choices=STATUS_ITEMS)
    created_time = models.DateTimeField("创建时间", auto_now_add=True)

    owner = models.ForeignKey(User, verbose_name=const.owner_name, on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = "侧边栏"
# -------------------------------------------------------------------------------------------------------------------- #
