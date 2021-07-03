from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    pass

class Follow(models.Model):
    follower= models.ForeignKey(User,on_delete=CASCADE,related_name="following")
    following = models.ForeignKey(User,on_delete=CASCADE,related_name="follower")

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE,related_name="user")
    post_content = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def serialize(self):
        return{
            "likes":self.likes
        }

class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=CASCADE,related_name="likedpost")
    user = models.ForeignKey(User,on_delete=CASCADE,related_name="likeduser")
