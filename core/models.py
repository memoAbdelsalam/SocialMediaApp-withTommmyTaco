from django.db import models
from django.contrib.auth import get_user_model # new
from datetime import datetime
import uuid # new

# Create your models here.

User = get_user_model() # new

class Profile(models.Model): # new
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	id_user = models.IntegerField()
	bio = models.TextField(blank=True)
	profile_img = models.ImageField(upload_to='profile_images', default='blank_profile_picture.jpg')
	location = models.CharField(blank=True, max_length=50)

	def __str__(self):
		return self.user.username


class Post(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	user = models.CharField(max_length=100)
	image = models.ImageField(upload_to='post_images')
	caption = models.TextField(null=True)
	created_at = models.DateTimeField(default=datetime.now)
	no_of_likes = models.IntegerField(default=0)

	def __str__(self):
		return self.user 


class LikePost(models.Model):
	post_id = models.CharField(max_length=500)
	username = models.CharField(max_length=200)

	def __str__(self):
		return self.username

class FollowersCount(models.Model):
	follower = models.CharField(max_length=500)
	user = models.CharField(max_length=200)

	def __str__(self):
		return self.user