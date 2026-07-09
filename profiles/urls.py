from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("edit/", views.edit_profile, name="edit_profile"),
    path("search/", views.search_users, name="search_users"),
    path("follow/<str:username>/", views.follow_user, name="follow_user"),
    path("<str:username>/", views.profile, name="profile"),
]