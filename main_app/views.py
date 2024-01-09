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
from .forms import ProfileForm, PostForm, CommentForm, PostForm
from django.urls import reverse_lazy

def calculate_time_since(post_date):
    now = timezone.now()
    time_difference = now - post_date
    seconds = time_difference.total_seconds()
    hours = seconds // 3600
    days = hours // 24
    weeks = days // 7
    years = days // 365

    if hours < 24:
        return f"{int(hours)}h"
    elif days < 7:
        return f"{int(days)}d"
    elif days < 365:
        return f"{int(weeks)}w"
    else:
        return f"{int(years)}y"

def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    posts_with_time = [(post, calculate_time_since(post.date_posted)) for post in posts]
    return render(request, 'home.html', {'posts_with_time': posts_with_time})

def profile(request, pk):
    profile = request.user.profile
    posts = Post.objects.filter(profile=profile).order_by('-date_posted')
    posts_with_time = [(post, calculate_time_since(post.date_posted)) for post in posts]
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

            post_photo = request.FILES.get('post-photo', None)

            if post_photo:
              s3 = boto3.client('s3')
              key = uuid.uuid4().hex[:6] + post_photo.name[post_photo.name.rfind('.'):]
              try:
                  bucket = os.environ['S3_BUCKET']
                  s3.upload_fileobj(post_photo, bucket, key)
                  url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                  post.post_photo = url
                  post.save()
                  Post_image.objects.create(url=url, post=post)
                  print(f"Image URL: {url}")
              except Exception as e:
                  print('An error occured uploading the image to S3')
                  print(e)
              return redirect('#', post=post)
    else:
        form = PostForm()

    return render(request, 'main_app/post_form.html', {'form': form})
      


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

    template_name = 'forms/profile_form.html'
    fields = ['profile_picture','bio']
    success_url = reverse_lazy('profile')

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.profile.pk})

class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.profile.pk})
    

class PostDelete(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.profile.pk})


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['time_since'] = calculate_time_since(post.date_posted)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.user = request.user
            comment.save()
            return redirect(self.object.get_absolute_url())


class CommentDelete(LoginRequiredMixin,DeleteView):
    model = Comment 
    template_name = "comment_confirm_delete.html"
    success_url = reverse_lazy('post_detail')
    
    def get_success_url(self):
        post = self.object.post
        return reverse('post_detail', kwargs={'pk': post.pk})
