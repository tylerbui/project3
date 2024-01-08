from django.forms import ModelForm
from django import forms
from .models import Profile, Post, Comment

class ProfileForm(ModelForm):
  class Meta:
    model = Profile
    fields = ['user', 'bio']

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['text_content', 'post_photo', 'post_tags']

class CommentForm(ModelForm):
  class Meta:
    model = Comment 
    fields = ['user','comment_text']