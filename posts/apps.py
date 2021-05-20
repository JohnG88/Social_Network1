from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
    # Below changed the Posts to Posts, Comments, Likes in admin
    # Also have to add default_app_config = 'posts.apps.PostsConfig' to init.py
    verbose_name = ' Posts, Comments, Likes'
    