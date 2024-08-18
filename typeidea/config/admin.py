from django.contrib import admin

from config.models import Link, SiderBar
from shared.modeladmin_mixin import SetOwnerToCurrentUserMixin


@admin.register(Link)
class LinkAdmin(SetOwnerToCurrentUserMixin, admin.ModelAdmin):
    list_display = ("title", "href", "status", "weight", "created_time")
    fields = ("title", "href", "status", "weight")

    def save_model(self, *args, **kwargs):
        return self.save_model_mixin(*args, **kwargs)


@admin.register(SiderBar)
class SiderBarAdmin(SetOwnerToCurrentUserMixin, admin.ModelAdmin):
    list_display = ("title", "display_type", "content", "status", "created_time")
    fields = ("title", "display_type", "content",)

    def save_model(self, *args, **kwargs):
        return self.save_model_mixin(*args, **kwargs)
