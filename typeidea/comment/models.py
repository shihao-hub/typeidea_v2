from django.db import models

from blog.models import Post
from shared.model_mixin import CommonModelMixin


# -------------------------------------------------------------------------------------------------------------------- #
class Comment(CommonModelMixin, models.Model):
    STATUS_NORMAL, STATUS_DELETE = 1, 0
    STATUS_ITEMS = ((STATUS_NORMAL, "正常"), (STATUS_DELETE, "删除"))

    content = models.CharField("内容", max_length=2000)
    nickname = models.CharField("昵称", max_length=50)
    website = models.URLField("网站", null=True, blank=True)  # (N)!: blank 是给表单用的，允许提交的表单对应项不填
    email = models.EmailField("邮箱", null=True, blank=True)
    status = models.PositiveIntegerField("状态", default=STATUS_NORMAL, choices=STATUS_ITEMS)
    created_time = models.DateTimeField("创建时间", auto_now_add=True)

    # (N)!: 2024-08-19，起初 target 没有添加，后续再添加的时候就必须要设置默认值了 或者 手动设置一下 或者 null=True
    target = models.ForeignKey(Post, verbose_name="评论目标", on_delete=models.DO_NOTHING, null=True)

    class Meta:
        verbose_name = verbose_name_plural = "评论"
# -------------------------------------------------------------------------------------------------------------------- #
