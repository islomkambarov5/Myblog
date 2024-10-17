from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

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

class PostList(ListView):
    model = Post
    extra_context = {
        'title': 'My blog',
        'posts': Post.published.all()
    }
    template_name = 'index.html'


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.ACTIVE,
                             publish__year=year, publish__month=month, publish__day=day, )
    context = {
        'title': 'Blog Post Detail',
        'post': post
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
