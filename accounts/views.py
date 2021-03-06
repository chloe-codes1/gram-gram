from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, JsonResponse
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import messages

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.add_message(request, messages.INFO, 'Welcome '+user.username +'!')
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.add_message(request, messages.INFO, 'Login Successfull!')
            return redirect(request.GET.get('next') or 'articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    messages.add_message(request, messages.SUCCESS, "You've been logged out.")
    return redirect('articles:index')

@login_required
def follow(request, username):
    person = get_object_or_404(User, username=username)
    user = request.user
    if user in person.followers.all():
        person.followers.remove(user)
        following = False
    else:
        person.followers.add(user)
        following = True
    context = {
        'following': following,
        'followingCount': person.followings.count(),
        'followerCount': person.followers.count(),
    }
    return JsonResponse(context)

def profile(request, username):
    #해당 유저 (username)의 정보를 보여줌
    person = get_object_or_404(User, username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)


def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context ={
        'form':form
    }
    return render(request, 'accounts/update.html', context)

@require_POST
@login_required
def delete(request):
    request.user.delete()
    messages.add_message(request, messages.ERROR, "Your account has been deleted.")
    return redirect('articles:index')