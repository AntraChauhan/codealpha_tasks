from django.contrib import admin
from .models import Post, Comment, Notification, Message


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "content", "created_at")
    list_filter = ("created_at",)
    search_fields = ("content", "author__username")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "content", "created_at")
    search_fields = ("content", "user__username")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "is_read", "created_at")
    list_filter = ("is_read",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "created_at")
