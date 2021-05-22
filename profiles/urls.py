from django.urls import path
from .views import my_profile_view, invites_received_view, profiles_list_view, invites_profiles_list_view

app_name = 'profiles'

# The first path will get the url to look like, http:127.0.0.1:8000/profiles/myprofile
# The first profile is from root views.py
urlpatterns = [
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('my-invites/', invites_received_view, name='my-invites-view'),
    path('all-profiles/', profiles_list_view, name='all-profiles-view'),
    path('to-invite/', invites_profiles_list_view, name='invite-profiles-view'),
]