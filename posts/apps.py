from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
    
    def ready(self):
        import posts.signals  # Asegúrate de que las señales se registren



class ProfilesConfig(AppConfig):
    name = 'profiles'

    def ready(self):
        import posts.signals  # Importa los signals cuando la aplicación esté lista
