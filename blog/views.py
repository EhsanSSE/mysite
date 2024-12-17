from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post, Comment
from django.core.paginator import Paginator
from blog.forms import CommentForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

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

    # Redirect if login is required
    if post.login_require and not request.user.is_authenticated:
        return redirect(f"{reverse('accounts:login')}?next={request.path}")

    # Increment post views
    post.counted_views += 1
    post.save()

    # Get next and previous posts
    previous_post, next_post = get_adjacent_posts(post)

    # Handle comment form
    form = handle_comment_form(request, post)

    # Fetch approved comments
    comments = Comment.objects.filter(post=post.id, approved=True)

    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/blog-single.html', context)

def get_adjacent_posts(post):
    """Get previous and next posts relative to the current post."""
    posts = list(Post.objects.filter(published_date__lte=timezone.now(), status=True).order_by('-published_date'))
    index_post = posts.index(post)
    previous_post = posts[index_post - 1] if index_post > 0 else None
    next_post = posts[index_post + 1] if index_post < len(posts) - 1 else None
    return previous_post, next_post

def handle_comment_form(request, post):
    """Handle the comment form submission."""
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your Comment submitted Successfully')
        else:
            messages.error(request, 'Your Comment Did not submit')
    else:
        form = CommentForm()
    return form


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

