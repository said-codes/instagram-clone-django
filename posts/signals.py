# posts/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F
from django.contrib.auth.models import User
from .models import Like, Follow, Profile

# Crear el perfil cuando un usuario nuevo se crea
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # Asegurarse de que el perfil siempre se guarde cuando el usuario se actualiza
        instance.profile.save()

# Incrementar contador de likes cuando se agrega un like
@receiver(post_save, sender=Like)
def increment_like_count(sender, instance, created, **kwargs):
    if created:
        instance.post.like_count = F('like_count') + 1
        instance.post.save(update_fields=['like_count'])

# Decrementar contador de likes cuando se elimina un like
@receiver(post_delete, sender=Like)
def decrement_like_count(sender, instance, **kwargs):
    if instance.post.like_count > 0:
        instance.post.like_count = F('like_count') - 1
        instance.post.save(update_fields=['like_count'])

# Incrementar contador de seguidores y siguiendo cuando alguien sigue a otro usuario
@receiver(post_save, sender=Follow)
def increment_follow_count(sender, instance, created, **kwargs):
    if created:
        followed_profile = Profile.objects.get(user=instance.followed)
        follower_profile = Profile.objects.get(user=instance.follower)
        followed_profile.follower_count = F('follower_count') + 1
        follower_profile.following_count = F('following_count') + 1
        followed_profile.save(update_fields=['follower_count'])
        follower_profile.save(update_fields=['following_count'])

# Decrementar contador de seguidores y siguiendo cuando alguien deja de seguir a otro usuario
@receiver(post_delete, sender=Follow)
def decrement_follow_count(sender, instance, **kwargs):
    followed_profile = Profile.objects.get(user=instance.followed)
    follower_profile = Profile.objects.get(user=instance.follower)
    
    if followed_profile.follower_count > 0:
        followed_profile.follower_count = F('follower_count') - 1
    if follower_profile.following_count > 0:
        follower_profile.following_count = F('following_count') - 1
    
    followed_profile.save(update_fields=['follower_count'])
    follower_profile.save(update_fields=['following_count'])
