from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post

@receiver(post_save, sender=Post)
def move_oldest_post_to_archive(sender, instance, **kwargs):
    posts = Post.objects.filter(is_featured=True).order_by('-created_at')
    if posts.count() > 3:
        oldest_post = posts.last()
        oldest_post.is_featured = False
        oldest_post.save()
