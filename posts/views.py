from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Follow, Like
from .forms import PostForm
from django.contrib.auth import logout
from .forms import ProfileUpdateForm, UserUpdateForm
from .forms import ProfileForm
from .models import Profile
from .models import Comment
from .forms import CommentForm


@login_required
def home(request):
    followed_users = Follow.objects.filter(
        follower=request.user).values_list('followed', flat=True)
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/home.html', {'posts': posts, 'followed_users': followed_users})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def follow(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if user_to_follow != request.user:
        Follow.objects.get_or_create(
            follower=request.user, followed=user_to_follow)
    return redirect('home')

@login_required
def unfollow(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    return redirect('home')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if created:
        post.like_count = post.like_count + 1  # Incrementa el contador
        post.save(update_fields=['like_count'])
    return redirect('home')

@login_required
def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Like.objects.filter(user=request.user, post=post).first()
    if like:
        like.delete()
        if post.like_count > 0:
            post.like_count = post.like_count - 1  # Decrementa el contador
            post.save(update_fields=['like_count'])
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    form.fields['username'].widget.attrs.update({'class': 'form-control'})
    form.fields['password'].widget.attrs.update({'class': 'form-control'})

    return render(request, 'registration/login.html', {'form': form})

def profile(request, username):
    posts = Post.objects.filter(user__username=username)
    return render(request, 'accounts/profile.html', {'posts': posts})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})



@login_required
def profile_settings(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Si no existe un perfil, lo creamos aquí (aunque debería manejarse automáticamente con las señales)
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('settings')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'accounts/profile_settings.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Tu cuenta ha sido eliminada.')
        logout(request)
        return redirect('home')
    return render(request, 'posts/delete_account.html')



@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if user_to_follow != request.user:
        Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
        # Actualizar el conteo en los perfiles
        profile = Profile.objects.get(user=user_to_follow)
        profile.follower_count += 1
        profile.save()

        user_profile = Profile.objects.get(user=request.user)
        user_profile.following_count += 1
        user_profile.save()
    return redirect('home', user_id=user_id)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    follow = Follow.objects.filter(follower=request.user, followed=user_to_unfollow)
    if follow.exists():
        follow.delete()
        # Actualizar el conteo en los perfiles
        profile = Profile.objects.get(user=user_to_unfollow)
        profile.follower_count -= 1
        profile.save()

        user_profile = Profile.objects.get(user=request.user)
        user_profile.following_count -= 1
        user_profile.save()
    return redirect('home', user_id=user_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('home')  # Puedes redirigir a 'post_detail' si prefieres
    else:
        form = CommentForm()
    return render(request, 'posts/add_comment.html', {'form': form, 'post': post})
