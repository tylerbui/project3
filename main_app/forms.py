from django.forms import ModelForm
from .models import Profile, Post

class ProfileForm(ModelForm):
  class Meta:
    model = Profile
    fields = ['user', 'bio']

class PostForm(ModelForm):
  class Meta:
    model = Post
    fields = ['text_content']