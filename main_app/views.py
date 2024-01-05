from django.shortcuts import render, redirect
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
#Remember to Include @login_required for certain classes in this view *** 
from django.contrib.auth.mixins import LoginRequiredMixin
#Remember to Include LoginRequiredMixin as a parameter to the classes that need it (ex. CreateView) (Class Base Views)
from .models import Post


# Create your views here.

def home(request):
    return render(request, 'home.html')

def create_post(request):
  posts = Post.objects.all()
  return render(request, 'main_app/create_post.html', {
    'posts': posts
  })

class PostCreate(CreateView):
  model = Post
  fields = ['content']


# Assigning post to a user 
# create a class 
    # def form_valid(self, form):
    #   form.instance.user = self.request.user 
    #   return super().form_valid(form)



# Added Auth Signup 
# Need to Link the Signup page in base.html 
# Also add a path for the URL signup 
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)