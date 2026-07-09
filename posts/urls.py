from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create_post, name="create_post"),
    path("like/<int:post_id>/", views.like_post, name="like_post"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),
    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),
    path("comment/<int:post_id>/", views.add_comment, name="add_comment"),
    path("notifications/", views.notifications, name="notifications"),
    path("chat/<str:username>/", views.chat, name="chat"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),

    # ✅ Add this
    path("search/", views.search_posts, name="search_posts"),
]