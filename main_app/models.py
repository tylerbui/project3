from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Profile(models.Model):
    profile_picture = models.URLField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="Bio +") 

    def __str__(self):
        return f'{self.user} ({self.id})'
    

class Post(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    text_content = models.TextField(max_length=250)
    post_photo = models.URLField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.user} ({self.id})'
    
class Comment(models.Model):
    content = models.TextField()
    image = models.URLField()
    post = models.ManyToManyField(Post)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} ({self.id})'






    


