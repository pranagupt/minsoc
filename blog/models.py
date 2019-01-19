from django.db import models
from django.contrib.auth.models import AbstractUser
from mysite.settings import AUTH_USER_MODEL

class CustomUser(AbstractUser):
    follows = models.ManyToManyField(AUTH_USER_MODEL)
    def __str__(self):
        return self.username

class Post(models.Model):
    is_deleted = models.BooleanField('is deleted?', default = False)
    is_before_edit = models.BooleanField('is before edit?', default = False)
    current_post_pk = models.IntegerField(default = 0)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, default = 1)
    post_text = models.CharField('Post text',max_length = 1000)
    pub_datetime = models.DateTimeField('Date and Time published', auto_now_add = True)
    def __str__(self):
        return self.post_text[:15] + '...'


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, default = 1)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    comment_text = models.CharField(max_length = 400)
    pub_datetime = models.DateTimeField('Date and Time published', auto_now_add = True)
    def __str__(self):
        return self.comment_text[:15] + '...'
