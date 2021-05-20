from django.urls import path
from .views import my_profile_view

app_name = 'profiles'

# The first path will get the url to look like, http:127.0.0.1:8000/profiles/myprofile
# The first profile is from root views.py
urlpatterns = [
    path('myprofile/', my_profile_view, name='my-profile-view'),
]