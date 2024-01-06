import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.contrib.auth import login 
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .models import Profile, Post, Comment, Post_image
from .forms import ProfileForm, PostForm

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

    # user_profile = Profile.objects.get(user=request.user)

    return render(request, 'home.html', {'posts_with_time': posts_with_time})

@login_required
def profile(request, pk):
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
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.profile = request.user.profile
            post.save()
            image_file = request.FILES.get('image-file', None)
            print("image file: {image_file}")
            if image_file:
              s3 = boto3.client('s3')
              key = uuid.uuid4().hex[:6] + image_file.name[image_file.name.rfind('.'):]
              try:
                  bucket = os.environ['S3_BUCKET']
                  s3.upload_fileobj(image_file, bucket, key)
                  url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                  Post_image.objects.create(url=url, post=post)
                  print(f"Image URL: {url}")
              except Exception as e:
                  print('An error occured uploading the image to S3')
                  print(e)
              return redirect('#', post=post)
    else:
        form = PostForm()

    return render(request, 'main_app/post_form.html')
      


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


class ProfileUpdate(LoginRequiredMixin,UpdateView):
    model = Profile
    template_name = 'forms/profile.html'
    fields = ['user','bio']

    def get_success_url(self):
        return reverse('profile_update', kwargs={'pk': self.request.user.profile.pk})

class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.profile.pk})
    