from django.contrib import admin


class SetOwnerToCurrentUserMixin:
    @staticmethod
    def generate_save_model(kls):
        """
            2024-08-19:
            此处算是复杂的函数提取了，《流畅的 Python》这本书还是很有用的（如果想进阶的话）
            1. super
            2. 调用时需要主动传入 self，保证 save_model(self, ...) <-> self.save_model(...)
            3. 混入类的方法中的 self 是混入类的实例，type(self) 生成的也只是混入类，所以此处用返回值是函数的方式来...
        """

        def save_model(self, *args, **kwargs):
            request, obj, form, change, *_ = args
            obj.owner = request.user
            # print("zsh -> ", type(request.user)) # <class 'django.utils.functional.SimpleLazyObject'>
            return super(kls, self).save_model(*args, **kwargs)

        return save_model

    @staticmethod
    def custom_save_model(kls, inst, *args, **kwargs):
        request, obj, form, change, *_ = args
        obj.owner = request.user
        # print("zsh -> ", type(request.user)) # <class 'django.utils.functional.SimpleLazyObject'>
        return super(kls, inst).save_model(*args, **kwargs)

    def save_model_mixin(self, *args, **kwargs):
        """ save 的时候设置 owner 为当前登录用户 """
        print("save_model_mixin:")
        request, obj, form, change, *_ = args
        obj.owner = request.user
        # (Q)!: 此处的 self 会定位到谁呢？我感觉这样写有问题啊...
        print(f"type(self): {type(self)}")
        return super(type(self), self).save_model(*args, **kwargs)
