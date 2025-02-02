# blog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Post, Tag, Resource, StaticPage
import logging

logger = logging.getLogger('django')

def landing_page(request):
    logger.debug('Accessing landing page')
    return render(request, 'blog/landing_page.html')

def homepage(request):
    logger.debug('Accessing blog homepage')
    # Retrieve recent posts and resources
    posts = Post.objects.all().order_by('-created_at')[:3]
    resources = Resource.objects.all()
    logger.debug(f'Found {len(posts)} recent posts')
    return render(request, 'blog/homepage.html', {
        'posts': posts,
        'resources': resources
    })

def posts_by_tag(request, tag_name):
    logger.debug(f'Fetching posts for tag: {tag_name}')
    tag = get_object_or_404(Tag, name=tag_name)
    posts = tag.posts.all().order_by('-created_at')
    logger.debug(f'Found {len(posts)} posts for tag {tag_name}')
    return render(request, 'blog/posts_by_tag.html', {
        'tag': tag, 
        'posts': posts
    })

def post_detail(request, pk):
    logger.debug(f'Accessing post detail for pk: {pk}')
    post = get_object_or_404(Post, pk=pk)
    related_posts = Post.objects.filter(category=post.category).exclude(pk=pk).order_by('-created_at')[:3]
    logger.debug(f'Found {len(related_posts)} related posts')
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'related_posts': related_posts
    })

def category_posts(request, category):
    logger.debug(f'Fetching posts for category: {category}')
    posts = Post.objects.filter(category=category).order_by('-created_at')
    logger.debug(f'Found {posts.count()} posts for category {category}')
    return render(request, 'blog/posts_by_tag.html', {
        'posts': posts, 
        'tag_name': category,  # Usiamo tag_name per mantenere compatibilità con il template
    })


def codeur_page(request):
    logger.debug('Accessing codeur page')
    page = get_object_or_404(StaticPage, page_type='CODEUR')
    return render(request, 'blog/codeur.html', {
        'page': page,
    })

def explorateur_page(request):
    logger.debug('Accessing explorateur page')
    page = get_object_or_404(StaticPage, page_type='EXPLORATEUR')
    return render(request, 'blog/explorateur.html', {
        'page': page,
    })