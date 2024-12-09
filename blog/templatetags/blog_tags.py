from django import template
from blog.models import Post, Comment
from blog.models import Category

register = template.Library()

@register.simple_tag(name='comments_count')
def function(pid):
    return Comment.objects.filter(post=pid, approved=True).count()

@register.simple_tag(name='totalpost')
def function():
    posts = Post.objects.filter(status=1)
    return posts

@register.filter
def snnipet(value, arg=20):
    return value[:arg] + '.......'

@register.inclusion_tag('blog/blog-latestposts.html')
def latestposts(arg=3):
    posts = Post.objects.filter(status=True).order_by('-published_date')[:arg]
    return {'posts': posts}


@register.inclusion_tag('blog/blog-postcategories.html')
def postcategories():
    posts = Post.objects.filter(status=True)
    categories = Category.objects.all()
    cat_dict = {}
    for name in categories:
        cat_dict[name] = posts.filter(category=name).count()

    return {'categories': cat_dict}