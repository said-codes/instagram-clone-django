# posts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow, name='unfollow'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('unlike/<int:post_id>/', views.unlike_post, name='unlike_post'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow, name='unfollow'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('accounts/settings/', views.profile_settings, name='settings'),
    path('accounts/delete/', views.delete_account, name='delete_account'),



]