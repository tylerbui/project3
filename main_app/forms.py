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

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['post_tags'].widget.attrs['placeholder']='Add a Tag'

class CommentForm(ModelForm):
  class Meta:
    model = Comment 
    fields = ['user','comment_text']