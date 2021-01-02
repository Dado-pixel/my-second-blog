from django.utils import timezone
from .models import Post, IP
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, Login
from django.contrib.auth.decorators import login_required, PermissionDenied, user_passes_test
import json
from datetime import timedelta
from django.utils.timezone import now
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from flask import request
from django.contrib.auth.models import User

def get_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip

@login_required
def post_list(request):
    last_ip = IP.objects.filter(User=request.user).latest('entr_date')
    form = Login(request.POST)
    if form.is_valid():
        new_ip = form.save(commit=False)
        new_ip.User = request.user
        new_ip.entr_date = timezone.now()
        new_ip.ip_address = get_ip(request)
        this_ip = IP.objects.filter(User=request.user).latest('entr_date')
        if this_ip != last_ip:
            messages.warning(request, 'Indirizzo ip diverso dal precedente.')
        new_ip.save()
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
            post.writeOnChain()
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

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/delete.html', {'post': post})

@superuser_only
def info_superuser(request):
    n = {}
    users_id = User.objects.all().values_list('id', flat=True)
    for x in users_id:
        posts = Post.objects.filter(author=x)
        n[x] =  len(posts)
    return render(request, 'blog/info_superuser.html', {'n': n})

@superuser_only
def last_hour_post(request):
    dt = now()
    PostsLastHour = Post.objects.filter(published_date__range=(dt-timedelta(hours=1), dt))
    post_1h = serializers.serialize('json',PostsLastHour)
    return HttpResponse(post_1h, content_type="text/json-comment-filtered")

@superuser_only
def search_str(request):
    template = 'blog/info_superuser.html'
    query = request.GET.get('q')
    results_title = Post.objects.filter(Q(title__icontains=query))
    results_text = Post.objects.filter(Q(text__icontains=query))
    n = len(results_text) + len(results_title)
    return HttpResponse(n)
