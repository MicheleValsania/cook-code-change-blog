from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from .models import Post, Tag, Resource
import logging
logger = logging.getLogger('django')

def homepage(request):
    logger.debug('Testing debug log')
    logger.error('Testing error log')
    # Retrieve both posts and resources
    posts = Post.objects.all().order_by('-created_at')[:3]
    resources = Resource.objects.all()
    return render(request, 'blog/homepage.html', {
        'posts': posts,
        'resources': resources
    })



def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = tag.posts.all().order_by('-created_at')  # Recupera i post associati al tag
    return render(request, 'blog/posts_by_tag.html', {'tag': tag, 'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Ottieni i post correlati della stessa categoria, ordinati per data
    related_posts = Post.objects.filter(category=post.category).exclude(pk=pk).order_by('-created_at')
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'related_posts': related_posts
    })


def category_posts(request, category):
    posts = Post.objects.filter(category=category).order_by('-created_at')
    print(f"Found {posts.count()} posts for category {category}")
    archive = Post.objects.filter(category=category).order_by('created_at')
    return render(request, 'blog/category_posts.html', {'posts': posts, 'category': category, 'archive': archive})
        
