from django import template
from blog.models import Post
from blog.models import Category

register = template.Library()

@register.simple_tag(name='totalpost')
def function():
    posts = Post.objects.filter(status=1)
    return posts

@register.filter
def snnipet(value, arg=20):
    return value[:arg] + '.......'

@register.inclusion_tag('blog/blog-latestposts.html')
def latestposts():
    posts = Post.objects.filter(status=True).order_by('-published_date')
    return {'posts': posts}


@register.inclusion_tag('blog/blog-postcategories.html')
def postcategories():
    posts = Post.objects.filter(status=True)
    categories = Category.objects.all()
    cat_dict = {}
    for name in categories:
        cat_dict[name] = posts.filter(category=name).count()

    return {'categories': cat_dict}