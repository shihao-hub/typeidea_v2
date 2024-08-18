from django.db import models


class AddObjectsFieldMixin:
    objects = models.Manager()


class CommonModelMixin(AddObjectsFieldMixin):
    """
        models.Model 的子类所需的一些自定义通用函数
    """

    def get_queryset(self, filter_dict=None):
        """ 根据不同的条件，获得当前查询对应的 queryset """
        res = self.objects.all()
        if filter_dict:
            res = res.filter(**filter_dict)
        return res

