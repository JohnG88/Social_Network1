from django import forms
from .models import Profile

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'email', 'country', 'friends', 'slug', 'updated', 'created')