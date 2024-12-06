from django import template
from blog.models import Post
from django.utils import timezone

register = template.Library()

@register.inclusion_tag('website/latest-blog-posts.html')
def latest_blog_posts():
    posts = Post.objects.filter(published_date__lte=timezone.now(), status=True).order_by('-published_date')
    

    return {'posts': posts}

