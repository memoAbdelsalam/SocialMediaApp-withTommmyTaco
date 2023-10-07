from django.urls import path
from . import views

urlpatterns= [
	path('', views.index, name='index'),
	path('signup', views.signup, name='signup'),
	path('signin', views.signin, name='signin'),
	path('logout', views.logout, name='logout'),

	path('settings', views.settings, name='settings'),
	path('upload', views.upload),

	path('profile/<str:pk>', views.profile, name='profile'),
	path('like-post', views.like_post, name='like-post'),
	path('follow', views.follow),

	path('search', views.search),

	path('test', views.test),
	path('suggest', views.suggest),
]

