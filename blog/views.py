from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from blog.models import Post, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def blog_view(request, **kwargs):
    posts = Post.objects.filter(published_date__lte=timezone.now(), status=True).order_by('-published_date')
    if kwargs.get('cat_name') != None:
        posts = posts.filter(category__name__iexact=kwargs.get('cat_name'))
    if kwargs.get('author_username') != None:
        posts = posts.filter(author__username=kwargs.get('author_username'))
    if kwargs.get('tag_name') is not None:
        posts = posts.filter(tags__name__in=[kwargs.get('tag_name')])

    
    paginator = Paginator(posts, 3)
    page_num = request.GET.get('page', 1)
    try:
        page_num = int(page_num)
        if page_num < 1 or page_num > paginator.num_pages:
            page_num = 1
    except ValueError:
        page_num = 1

    posts = paginator.get_page(page_num)
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)

def blog_single(request, pk):
    post = get_object_or_404(Post, pk=pk, status=True) 
    post.counted_views += 1
    post.save()
    posts = list(Post.objects.filter(published_date__lte=timezone.now(), status=True).order_by('-published_date'))
    index_post = posts.index(post)
    previous_post = None
    next_post = None
    if index_post > 0:
        previous_post = posts[index_post - 1]
    if index_post < len(posts) - 1:
        next_post = posts[index_post + 1]
    comments = Comment.objects.filter(post=post.id, approved=True)
    context = {'post': post, 'previous_post': previous_post, 'next_post': next_post, 'comments': comments}
    return render(request, 'blog/blog-single.html', context)


def test_view(request):
    return render(request, 'test.html')


def blog_search(request):
    posts = Post.objects.filter(published_date__lte=timezone.now(), status=True).order_by('-published_date')
    if request.method == 'GET':
        # print(request.GET.get('s'))
        if s:= request.GET.get('s'):
            posts = posts.filter(content__contains=s)
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)

