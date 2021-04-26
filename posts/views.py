from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User, Follow
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    latest = group.posts.all()
    paginator = Paginator(latest, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "posts/group.html", {"group": group,
                                                "page": page})


@login_required(redirect_field_name='login')
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, 'posts/new.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/new.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    author_posts = author.posts.all()
    paginator = Paginator(author_posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = (request.user.is_authenticated
                 and Follow.objects.filter(user=request.user,
                                           author=author).exists())
    context = {'author': author,
               'author_posts': author_posts,
               'page': page,
               'following': following,
               }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    user = get_object_or_404(User, username=username)
    author_posts = user.posts.all()
    posts_count = author_posts.count()
    post = get_object_or_404(Post, id=post_id)
    authorized_user = request.user
    author = post.author
    image = post.image
    form = CommentForm(request.POST or None)
    comments = post.comments.all()
    return render(request, 'post.html', {
        'image': image,
        'post': post,
        'posts_count': posts_count,
        'authorized_user': authorized_user,
        'username': username,
        'author': author,
        'form': form,
        'comments': comments,
    })


@login_required
def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author=profile, pk=post_id)
    if request.user != profile:
        return redirect('post_profile', username=username, post_id=post_id)
    # добавим в form свойство files
    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect("post_profile", username=request.user.username,
                            post_id=post_id)

    return render(
        request, 'new.html', {'form': form, 'post': post},
    )


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    form = CommentForm(request.POST or None)
    context = {'form': form, 'post': post}
    if not form.is_valid():
        return render(request, 'comments.html', context)
    form.instance.author = request.user
    comment = form.save(commit=False)
    comment.post = post
    comment.save()
    return redirect('post_profile', username=username, post_id=post_id)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {'page': page})


@login_required
def profile_follow(request, username):
    author = User.objects.get(username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user,
                                     author=author)
        return redirect(reverse('profile', args=[username]))
    return redirect(reverse('profile', args=[username]))


@login_required
def profile_unfollow(request, username):
    unfollow_user = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=unfollow_user).delete()
    return redirect('profile', username=username)
