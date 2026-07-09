from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.db.models import Q

from .models import Post, Comment, Notification, Message
from .forms import PostForm, CommentForm, MessageForm
from django.core.paginator import Paginator


def home(request):
    if request.user.is_authenticated:
        following = request.user.following.all()
        posts = Post.objects.filter(
            Q(author=request.user) | Q(author__in=following)
        ).order_by("-created_at")
        suggestions = User.objects.exclude(id=request.user.id).exclude(
            profile__followers=request.user
        )[:5]
    else:
        posts = Post.objects.all().order_by("-created_at")
        suggestions = User.objects.all()[:5]

    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "posts/home.html", {
        "posts": page_obj,
        "suggestions": suggestions,
        "page_obj": page_obj,
    })


def create_post(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts:home")
    else:
        form = PostForm()

    return render(request, "posts/create_post.html", {"form": form})


def like_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        if request.user != post.author:
            Notification.objects.create(
                user=post.author,
                message=f"{request.user.username} liked your post ❤️"
            )

    return redirect("posts:home")


def edit_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("You cannot edit this post.")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts:home")
    else:
        form = PostForm(instance=post)

    return render(request, "posts/edit_post.html", {"form": form})


def delete_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("You cannot delete this post.")

    post.delete()
    return redirect("posts:home")


def add_comment(request, post_id):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            if request.user != post.author:
                Notification.objects.create(
                    user=post.author,
                    message=f"{request.user.username} commented on your post 💬"
                )

    return redirect("posts:home")


def notifications(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    notifs = request.user.notifications.order_by("-created_at")
    notifs.update(is_read=True)

    return render(request, "posts/notifications.html", {"notifications": notifs})


def chat(request, username):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    other_user = get_object_or_404(User, username=username)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("created_at")

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = other_user
            msg.save()
            return redirect("posts:chat", username=other_user.username)
    else:
        form = MessageForm()

    return render(request, "posts/chat.html", {
        "messages": messages,
        "form": form,
        "other_user": other_user,
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "posts/post_detail.html", {"post": post})


def search_posts(request):
    query = request.GET.get("q")
    posts = Post.objects.all().order_by("-created_at")

    if query:
        posts = Post.objects.filter(
            Q(content__icontains=query) | Q(author__username__icontains=query)
        ).order_by("-created_at")

    return render(request, "posts/search_posts.html", {
        "posts": posts,
        "query": query,
    })
