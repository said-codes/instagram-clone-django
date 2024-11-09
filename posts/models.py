from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Publicación del usuario
    image = models.ImageField(upload_to='posts/')  # Imagen subida
    caption = models.TextField()  # Descripción de la imagen
    location = models.CharField(max_length=255, blank=True, null=True)  # Campo opcional de ubicación
    tags = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    like_count = models.PositiveIntegerField(default=0)  # Número de likes

    def __str__(self):
        return f"Post by {self.user.username}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.id}"

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followed', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=255, blank=True)
    follower_count = models.PositiveIntegerField(default=0)  # Número de seguidores
    following_count = models.PositiveIntegerField(default=0)  # Número de personas seguidas

    def __str__(self):
        return f"Profile of {self.user.username}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"



class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario propietario de la historia
    image = models.ImageField(upload_to='stories/')  # Imagen de la historia
    video = models.FileField(upload_to='stories/', blank=True, null=True)  # Video de la historia (opcional)
    caption = models.CharField(max_length=255, blank=True, null=True)  # Pie de foto (opcional)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    expires_at = models.DateTimeField()  # Fecha de expiración (generalmente 24 horas después de la creación)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

    def is_expired(self):
        return timezone.now() > self.expires_at
