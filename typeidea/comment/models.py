from django.db import models

from blog.models import Post
from shared.model_mixin import CommonModelMixin


# -------------------------------------------------------------------------------------------------------------------- #
class Comment(CommonModelMixin, models.Model):
    STATUS_NORMAL, STATUS_DELETE = 1, 0
    STATUS_ITEMS = ((STATUS_NORMAL, "正常"), (STATUS_DELETE, "删除"))

    content = models.CharField("内容", max_length=2000)
    nickname = models.CharField("昵称", max_length=50)
    website = models.URLField("网站", null=True)
    email = models.EmailField("邮箱", null=True)
    status = models.PositiveIntegerField("状态", default=STATUS_NORMAL, choices=STATUS_ITEMS)
    created_time = models.DateTimeField("创建时间", auto_now_add=True)

    target = models.ForeignKey(Post,verbose_name="评论目标")

    class Meta:
        verbose_name = verbose_name_plural = "评论"
# -------------------------------------------------------------------------------------------------------------------- #
