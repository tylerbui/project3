from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.URLField()
    bio = models.TextField(max_length=40) 

    def __str__(self):
        return f'{self.user} ({self.id})'

class Post(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    text_content = models.TextField(max_length=250)
    post_photo = models.URLField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.user.username} ({self.id})'
    
    def save(self, *args, **kwargs):
        if self.user and self.user.profile:
            self.profile = self.user.profile
        super().save(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField(max_length=150)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post} ({self.id})'
    
def user_save(self, *args, **kwargs):
    created = not self.pk
    super(User, self).save(*args, **kwargs)
    if created:
        Profile.objects.create(user=self)

User.save = user_save