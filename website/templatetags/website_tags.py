from django import template
from blog.models import Post

register = template.Library()

@register.inclusion_tag('website/latest-blog-posts.html')
def latest_blog_posts():
    posts = Post.objects.filter(status=True).order_by('-published_date')
    return {'posts': posts}

