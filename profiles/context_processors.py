from .models import Profile

def profile_pic(request):
    if request.user.is_authenticated:
        