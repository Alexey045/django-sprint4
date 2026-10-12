from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CommentForm, PostForm, ProfileForm
from .models import Category, Comment, Post

POSTS_PER_PAGE = 10


def public_posts():
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    ).select_related("author", "category", "location").annotate(
        comment_count=Count("comments")
    ).order_by("-pub_date")


def visible_post(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related("author", "category", "location").annotate(
            comment_count=Count("comments")
        ),
        pk=post_id,
    )
    if request.user == post.author:
        return post
    if (
        post.is_published
        and post.pub_date <= timezone.now()
        and post.category
        and post.category.is_published
    ):
        return post
    raise Http404


def page_of(request, items):
    return Paginator(items, POSTS_PER_PAGE).get_page(request.GET.get("page"))


def index(request):
    return render(
        request,
        "blog/index.html",
        {"page_obj": page_of(request, public_posts())},
    )


def post_detail(request, id):
    post = visible_post(request, id)
    comments = post.comments.select_related("author").order_by("created_at")
    return render(
        request,
        "blog/detail.html",
        {"post": post, "comments": comments, "form": CommentForm()},
    )


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    posts = public_posts().filter(category=category)
    return render(
        request,
        "blog/category.html",
        {"category": category, "page_obj": page_of(request, posts)},
    )


def profile(request, username):
    profile_user = get_object_or_404(get_user_model(), username=username)
    posts = Post.objects.filter(author=profile_user).select_related(
        "author", "category", "location"
    ).annotate(comment_count=Count("comments")).order_by("-pub_date")
    if request.user != profile_user:
        posts = posts.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )
    return render(
        request,
        "blog/profile.html",
        {"profile": profile_user, "page_obj": page_of(request, posts)},
    )


@login_required
def create_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("blog:profile", username=request.user.username)
    return render(request, "blog/create.html", {"form": form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect("blog:post_detail", id=post.id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("blog:post_detail", id=post.id)
    return render(request, "blog/create.html", {"form": form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect("blog:post_detail", id=post.id)
    form = PostForm(instance=post)
    if request.method == "POST":
        post.delete()
        return redirect("blog:profile", username=request.user.username)
    return render(request, "blog/create.html", {"form": form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect("blog:post_detail", id=post.id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post_id=post_id)
    if request.user != comment.author:
        return redirect("blog:post_detail", id=post_id)
    form = CommentForm(request.POST or None, instance=comment)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("blog:post_detail", id=post_id)
    return render(
        request,
        "blog/comment.html",
        {"comment": comment, "form": form},
    )


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post_id=post_id)
    if request.user != comment.author:
        return redirect("blog:post_detail", id=post_id)
    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", id=post_id)
    return render(
        request,
        "blog/comment.html",
        {"comment": comment},
    )


@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("blog:profile", username=request.user.username)
    return render(request, "blog/user.html", {"form": form})


def registration(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("login")
    return render(
        request,
        "registration/registration_form.html",
        {"form": form},
    )
