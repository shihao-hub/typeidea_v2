from django.contrib import admin
from django.contrib.admin.models import LogEntry

from config.models import Link, SiderBar
from shared.modeladmin_mixin import SetOwnerToCurrentUserMixin
from typeidea.custom_site import custom_admin_site


@admin.register(LogEntry, site=custom_admin_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("object_repr", "object_id", "action_flag", "user", "change_message",)


# -------------------------------------------------------------------------------------------------------------------- #
@admin.register(Link, site=custom_admin_site)
class LinkAdmin(SetOwnerToCurrentUserMixin, admin.ModelAdmin):
    list_display = ("title", "href", "status", "weight", "created_time")
    fields = ("title", "href", "status", "weight")

    def save_model(self, *args, **kwargs):
        return self.save_model_mixin(*args, **kwargs)


@admin.register(SiderBar, site=custom_admin_site)
class SiderBarAdmin(SetOwnerToCurrentUserMixin, admin.ModelAdmin):
    list_display = ("title", "display_type", "content", "status", "created_time")
    fields = ("title", "display_type", "content",)

    def save_model(self, *args, **kwargs):
        return self.save_model_mixin(*args, **kwargs)
