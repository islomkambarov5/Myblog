from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

from mySite import settings
from .models import *
from .forms import *


# Create your views here.

# def index(request):
#     try:
#         posts = Post.published.all()
#     except Post.DoesNotExist:
#         raise Http404("Post doesn't exist")
#     context = {
#         'title': 'My blog',
#         'posts': posts
#     }
#     return render(request, 'index.html', context)

# class PostList(ListView):
#     model = Post
#     extra_context = {
#         'title': 'My blog',
#         'posts': Post.published.all()
#     }
#     template_name = 'index.html'

def index(request):
    return render(request, 'index.html', {'title': 'My blog', 'posts': Post.published.all(), 'tags': Tag.objects.all()})

def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    context = {
        'title': 'My blog',
        'posts': posts
    }

    
    return render(request, 'index_taggir.html', context)

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.ACTIVE,
                             publish__year=year, publish__month=month, publish__day=day)
    
    post_tags = post.tags.values_list('id', flat=True)
    comments = post.comments.all()
    similar_posts = (Post.published
                     .filter(tags__in=post_tags)
                     .exclude(id=post.id)
                     .annotate(same_tags=Count('tags'))
                     .order_by('-same_tags', '-publish')
                     .distinct()[:4])
    
    context = {
        'title': 'Blog Post Detail',
        'post': post,
        'form': CommentForm(),
        'similar_posts': similar_posts,
        'comments': comments
    }
    return render(request, 'post_detail.html', context)


def post_share(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.ACTIVE)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']}, вам пришло новое сообщение!"
            message = f"Посетите ``{post.title}`` по ссылке {post_url}"
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[cd['to']],
                fail_silently=False
            )
            return redirect('index')
    else:
        form = EmailPostForm
    context = {
        'title': 'Share with link',
        'form': form
    }
    return render(request, 'post_share.html', context)


@require_POST
def comment_create(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.ACTIVE)
    form = CommentForm(request.POST)
    comment = None

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect(post.get_absolute_url())

    return render(request, 'post_comment.html', {
        'title': 'Comment Creating Page',
        'form': form,
        'comment': comment,
    })

def search_with_indexing(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(title__icontains=query)
        context = {
            'title': 'Search results',
            'posts': posts,
            'query': query,
            'tags': Tag.objects.all()
        }
        return render(request,'index.html', context)
    else:
        return redirect('index')
