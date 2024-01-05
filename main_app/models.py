from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    profile_picture = models.URLField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20)
    bio = models.TextField(default="Bio +") 

    def __str__(self):
        return f'{self.user_name} ({self.id})'
    

class Post(models.Model): 
    profile_picture = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_name} ({self.id})'
    
class Comment(models.Model):
    content = models.TextField()
    image = models.URLField()
    post = models.ManyToManyField(Post)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_name} ({self.id})'


class Photo(models.Model):
    url = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.id})'
    