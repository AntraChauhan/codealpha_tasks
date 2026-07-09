from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

from .models import Profile
from .forms import ProfileForm
from posts.models import Post, Notification


def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    posts = Post.objects.filter(author=user).order_by("-created_at")

    return render(request, "profiles/profile.html", {
        "profile": profile,
        "posts": posts,
        "posts_count": posts.count(),
        "followers_count": profile.followers.count(),
        "following_count": user.following.count(),
        "total_likes": sum(p.likes.count() for p in posts),
    })


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profiles:profile", username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profiles/edit_profile.html", {"form": form})


def follow_user(request, username):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    user = get_object_or_404(User, username=username)
    profile = user.profile

    if request.user != user:
        if request.user in profile.followers.all():
            profile.followers.remove(request.user)
        else:
            profile.followers.add(request.user)
            Notification.objects.create(
                user=user,
                message=f"{request.user.username} started following you 👤"
            )

    return redirect("profiles:profile", username=username)


def search_users(request):
    query = request.GET.get("q")
    users = User.objects.filter(username__icontains=query) if query else []

    return render(request, "profiles/search.html", {
        "users": users,
        "query": query,
    })
