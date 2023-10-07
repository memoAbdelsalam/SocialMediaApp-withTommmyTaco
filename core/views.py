from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Post, LikePost, FollowersCount
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
# Create your views here.


def suggest(request):
	users = User.objects.all()
	profiles = Profile.objects.all()

	user_following_list = []

	user_following = FollowersCount.objects.filter(follower=request.user.username) # FollowersCount objects which express following
	for user in user_following:
		user_following_list.append(user.user)

	# user_following_list = list(chain(*user_following_list))
	random.shuffle(user_following_list)

	context = {
		'users':users,
		'user_following_list':user_following_list,
		# 'user_following':user_following,
		'profiles':profiles[:5],
	}
	return render(request, 'suggest.html', context)


def test(request):
	user_following_list = []
	feed = []

	user_following = FollowersCount.objects.filter(follower=request.user.username)
	for user in user_following:
		user_following_list.append(user.user)

	for username in user_following_list:
		feed.append(Post.objects.filter(user=username))

	new_feed = list(chain(*feed))

	context = {
		'user_following_list':user_following_list,
		'feed':feed,
		'new_feed':new_feed,
	}
	return render(request, 'test.html', context)

@login_required(login_url='signin')
def index(request):
	user_object = User.objects.get(username=request.user.username)
	user_profile = Profile.objects.get(user=user_object)
	posts = Post.objects.all()

	user_following_list = []
	feed = []

	user_following = FollowersCount.objects.filter(follower=request.user.username) # FollowersCount objects which express following
	for user in user_following:
		user_following_list.append(user.user)

	for username in user_following_list:
		feed.append(Post.objects.filter(user=username))

	feed = list(chain(*feed))

	# sugestion
	users = User.objects.all()
	profiles = Profile.objects.all()

	user_following_list = []

	user_following = FollowersCount.objects.filter(follower=request.user.username) # FollowersCount objects which express following
	for user in user_following:
		user_following_list.append(user.user)

	context = {
		'user_profile':user_profile,
		'posts':feed,
		'users':users,
		'user_following_list':user_following_list,
		'user_following':user_following,
		'profiles':profiles,
		# 'final_suggestion_list':final_suggestion_list[:4],
	}
	return render(request, 'index.html', context)



@login_required(login_url='signin')
def profile(request, pk):
	user_object = User.objects.get(username=pk)
	user_profile = Profile.objects.get(user=user_object)
	user_posts = Post.objects.filter(user=pk)
	user_posts_length = len(user_posts)

	follower = request.user.username
	user = pk
	if FollowersCount.objects.filter(follower=follower,user=user).first():
		button_text = 'Unfollow'
	else:
		button_text = 'Follow'

	user_followers = len(FollowersCount.objects.filter(user=pk))
	user_following = len(FollowersCount.objects.filter(follower=pk))

	context = {
	'user_object':user_object,
	'user_profile':user_profile,
	'user_posts':user_posts,
	'user_posts_length':user_posts_length,
	'button_text':button_text,
	'user_followers':user_followers,
	'user_following':user_following,
	}
	return render(request, 'profile.html', context)

def signup(request):

	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		password2 = request.POST['password2']

		if password==password2:
			if User.objects.filter(email=email).exists():
				messages.info(request, 'email already exists')
				return redirect('signup')
			elif User.objects.filter(username=username).exists():
				messages.info(request, 'username already exists')
				return redirect('signup')
			else:
				user = User.objects.create_user(username=username,email=email,password=password)
				user.save()

				# log user in & redirect to settings page
				user_login = auth.authenticate(username=username,password=password)
				auth.login(request,user_login)

				# create a profile pbject for the new user
				user_model = User.objects.get(username=username)
				new_profile = Profile.objects.create(user=user_model,id_user=user_model.id)
				new_profile.save()
				return redirect("settings")
		else:
			messages.info(request, 'passwords don\'t match')
			return redirect('signup')
	else:	
		return render(request, 'signup.html')
		


def signin(request):

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username=username,password=password)
		
		if user is not None:
			auth.login(request,user)
			return redirect("/")
		else:
			messages.info(request, 'credentials Invalid')
			return redirect('signin')

	else:	
		return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request):
	auth.logout(request)
	return redirect('signin')

@login_required(login_url='signin')
def settings(request):
	user_profile = Profile.objects.get(user=request.user)

	if request.method == 'POST':

		if request.FILES.get('image') == None:
			bio = request.POST['bio']
			location = request.POST['location']
			
			user_profile.bio = bio
			user_profile.location = location
			user_profile.save()

		elif request.FILES.get('image') != None:
			image = request.FILES['image']
			bio = request.POST['bio']
			location = request.POST['location']

			user_profile.profile_img = image
			user_profile.bio = bio
			user_profile.location = location
			user_profile.save()

		return redirect('settings')

	return render(request, 'settings.html', {'user_profile':user_profile})



def upload(request):

	if request.method == 'POST':
		user = request.user.username
		image = request.FILES.get('image_upload')
		caption = request.POST['caption']

		new_post = Post.objects.create(user=user, image=image, caption=caption)
		new_post.save()
		return redirect('/')
	else:
		return redirect('/')


@login_required(login_url='signin')
def like_post(request):
	username = request.user.username
	post_id = request.GET['post_id']

	post = Post.objects.get(id=post_id)

	like_filter = LikePost.objects.filter( post_id=post_id,username=username).first()

	if like_filter == None :
		newLike = LikePost.objects.create(post_id=post_id,username=username)
		newLike.save()
		post.no_of_likes += 1
		post.save()
		return redirect('/')
	else:
		like_filter.delete()
		post.no_of_likes -= 1
		post.save()
		return redirect('/')



@login_required(login_url='signin')
def follow(request):
	if request.method == 'POST':
		follower = request.POST['follower']
		user = request.POST['user']

		if FollowersCount.objects.filter(follower=follower,user=user).first():
			delete_follower = FollowersCount.objects.get(follower=follower,user=user)
			delete_follower.delete()
			return redirect('/profile/' + user)
		else:
			new_follower = FollowersCount.objects.create(follower=follower,user=user)
			new_follower.save()
			return redirect('/profile/' + user)
	else:
		pass 


def search(request):

	search = request.GET['search'] if request.GET['search'] != None else ''

	profiles = Profile.objects.filter(user__username__icontains=search)

	feed_search = []

	for profile in profiles:
		feed_search.append(Post.objects.filter(user=profile.user.username))
	feed_search = list(chain(*feed_search))

	user = request.user
	user_profile = Profile.objects.get(user=user)

	context= {
		'posts':feed_search, 'profiles':profiles, 'user_profile':user_profile, 'search':search
	}

	return render(request, 'search.html', context)

