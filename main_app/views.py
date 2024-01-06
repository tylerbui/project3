from django.shortcuts import render, redirect
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .models import Profile, Post, Comment
from .forms import ProfileForm

def home(request):
    posts = Post.objects.all()
    now = timezone.now()

    posts_with_time = []
    for post in posts:
        time_difference = now - post.date_posted
        seconds = time_difference.total_seconds()
        hours = seconds // 3600
        days = hours // 24
        weeks = days // 7
        years = days // 365

        if hours < 24:
            time_since = f"{int(hours)}h"
        elif days < 7:
            time_since = f"{int(days)}d"
        elif days < 365:
            time_since = f"{int(weeks)}w"
        else:
            time_since = f"{int(years)}y"

        posts_with_time.append((post, time_since))

    return render(request, 'home.html', {'posts_with_time': posts_with_time})

@login_required
def profile(request):
    now = timezone.now()
    profile = request.user.profile
    posts = Post.objects.filter(profile=profile)

    posts_with_time = []
    for post in posts:
        time_difference = now - post.date_posted
        seconds = time_difference.total_seconds()
        hours = seconds // 3600
        days = hours // 24
        weeks = days // 7
        years = days // 365

        if hours < 24:
            time_since = f"{int(hours)}h"
        elif days < 7:
            time_since = f"{int(days)}d"
        elif days < 365:
            time_since = f"{int(weeks)}w"
        else:
            time_since = f"{int(years)}y"

        posts_with_time.append((post, time_since))

    return render(request, 'profile.html', {'profile': profile, 'posts_with_time': posts_with_time})

@login_required
def ProfileUpdate(LoginRequiredMixin,UpdateView):
   model = Profile
   fields = ['name','bio']
   

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)