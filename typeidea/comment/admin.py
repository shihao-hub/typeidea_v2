from django.contrib import admin

from comment.models import Comment
from shared.modeladmin_mixin import SetOwnerToCurrentUserMixin
from typeidea.custom_site import custom_admin_site


@admin.register(Comment, site=custom_admin_site)
class CommentAdmin(SetOwnerToCurrentUserMixin, admin.ModelAdmin):
    list_display = ("target", "content", "nickname", "website", "email", "status", "created_time")

    def save_model(self, *args, **kwargs):
        return self.save_model_mixin(*args, **kwargs)
