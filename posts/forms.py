from django import forms
from .models import Post, Profile
from django.contrib.auth.models import User

# Formulario para la creación de publicaciones
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption', 'location', 'tags']

# Formulario para la creación de usuario
class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

# Formulario para el perfil del usuario (agregar avatar, biografía, etc.)
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'location']

    # Validaciones personalizadas (si es necesario)
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            max_size = 5 * 1024 * 1024  # 5MB
            if avatar.size > max_size:
                raise forms.ValidationError("El tamaño de la imagen no puede ser mayor a 5MB.")
        return avatar

# Formulario para actualizar el perfil del usuario
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'location']

# Formulario para actualizar los datos del usuario
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
