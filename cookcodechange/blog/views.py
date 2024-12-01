from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from .models import Post, Tag

def homepage(request):
    # Retrieve the 5 most recent posts
    posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'blog/homepage.html', {'posts': posts})


def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = tag.posts.all().order_by('-created_at')  # Recupera i post associati al tag
    return render(request, 'blog/posts_by_tag.html', {'tag': tag, 'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def archive(request, section):
    posts = Post.objects.filter(tags__name=section).order_by('-created_at')
    return render(request, 'blog/archive.html', {'posts': posts, 'section': section})

def category_posts(request, category):
    posts = Post.objects.filter(tags__name=category).order_by('-created_at')
    return render(request, 'blog/category_posts.html', {'posts': posts, 'category': category})
