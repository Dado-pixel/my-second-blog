from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.models import Post
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm

def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(".")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip

def login_view(request):
    ip = get_ip(request)
    next = request.GET.get('next')
    title = 'Login'
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username');
        password = form.cleaned_data.get('password');
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    return render(request, 'login.html', {'form': form, 'title': title})

def register_view(request):
    next = request.GET.get('next')
    title = 'Registrazione'
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=user.password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    return render(request, 'account_form.html', {'form': form, 'title': title})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def profile(request, user, id):
    users = User.objects.get(username=user)
    id = User.objects.get(id=id)
    contex = {
        "id": id,
        "user": users
    }
    return render(request, 'profile/profile.html', contex)
