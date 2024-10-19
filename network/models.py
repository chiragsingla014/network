from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def follow(self, user):
        Follow.objects.get_or_create(follower=self, followee=user)

    def unfollow(self, user):
        Follow.objects.filter(follower=self, followee=user).delete()

    def is_following(self, user):
        if self == user:
            return False
        return Follow.objects.filter(follower=self, followee=user).exists()

    def is_followed_by(self, user):
        return Follow.objects.filter(follower=user, followee=self).exists()
    
    def __str__(self):
        return f'{self.username}'
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username
        }



class Post(models.Model):
    user = models.ForeignKey(User, related_name='psots', on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} posted this on {self.timestamp} having {self.likes} likes'
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.serialize(),
            "content": self.content,
            "likes": self.likes,
            "timestamp": self.timestamp,
        }



class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followee')

    def __str__(self):
        return f"{self.follower.username} follows {self.followee.username}"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def number_of_followers(self):
        return Follow.objects.filter(followee=self.user).count()

    def list_of_followers(self):
        return Follow.objects.filter(followee=self.user).values_list('follower', flat=True)
    
    def number_of_followings(self):
        return Follow.objects.filter(follower=self.user).count()

    def list_of_followings(self):
        return Follow.objects.filter(follower=self.user).values_list('followee', flat=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    
    
class Like(models.Model):
    liker = models.ForeignKey(User, related_name='likedposts', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likers', on_delete=models.CASCADE)

    def __str__ (self):
        return f"{self.liker.username} likes {self.post}"
    
    def isliking(user, post):
        return Like.objects.filter(liker=user, post=post).exists()