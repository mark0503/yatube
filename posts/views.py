from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group
from .forms import PostForm


def index(request):
    latest = Post.objects.order_by('-pub_date')[:11]
    return render(request, 'posts/index.html', {'posts': latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request, "posts/group.html", {"group": group,
                                                "posts": posts})


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

