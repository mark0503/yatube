from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    latest = Post.objects.order_by('-pub_date')
    paginator = Paginator(latest, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/index.html', {'page': page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request, "posts/group.html", {"group": group,
                                                "posts": posts})


@login_required(redirect_field_name='login')
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, 'posts/new.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/new.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    posts_count = Post.objects.filter(author=user).count()
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'username': user, 'posts_count': posts_count, 'page': page})


def post_view(request, username, post_id):
    user = get_object_or_404(User, username=username)
    author_posts = Post.objects.filter(author=user)
    posts_count = len(author_posts)
    post = get_object_or_404(Post, id=post_id)
    authorized_user = request.user
    author = post.author
    return render(request, 'post.html', {
        'post': post,
        'posts_count': posts_count,
        'authorized_user': authorized_user,
        'username': username,
        'author': author,
    })


def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user.id is not post.author.id:
        return redirect('post', username=username, post_id=post_id)
    PostForm(request.GET, instance=post)
    form = PostForm(request.POST or None, instance=post)
    if not form.is_valid():
        return render(request, "new.html", {"form": form, 'post': post})
    form.save()
    return redirect('post', username=username, post_id=post_id)
