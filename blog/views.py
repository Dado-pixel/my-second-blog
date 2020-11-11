from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required, PermissionDenied
from django.contrib.auth.models import User
import json
from datetime import timedelta
from django.utils.timezone import now
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q

@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def superuser_only(function):

    def _inner(request):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request)
    return _inner


@superuser_only
def info_superuser(request):
    numero = {}
    utenti = User.objects.all().values_list('id', flat=True)
    for utente in utenti:
        posts = Post.objects.filter(author=utente)
        numero[utente] =  len(posts)

    return render(request, 'blog/info_superuser.html', {'numero': numero})

@superuser_only
def PostUltimaOra(request):
    dt = now()
    PostsLastHour = Post.objects.filter(published_date__range=(dt-timedelta(hours=1), dt))
    post_1h = serializers.serialize('json',PostsLastHour)
    return HttpResponse(post_1h, content_type="text/json-comment-filtered")

@superuser_only
def CercaStringa(request):
    template = 'blog/info_superuser.html'

    query = request.GET.get('q')

    results_title = Post.objects.filter(Q(title__icontains=query))
    results_text = Post.objects.filter(Q(text__icontains=query))
    volte = len(results_text) + len(results_title)

    return HttpResponse(volte)
