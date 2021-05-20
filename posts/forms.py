from django import forms
from .models import Post, Comment

class PostModelForm(forms.ModelForm):
    # Line below creates the textfield to only two rows thick
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model = Post
        exclude = ('liked', 'updated', 'created', 'author')

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))
    class Meta:
        model = Comment
        # If there is inly one item, put a , at the end of the quoted word, because it is a tuple
        exclude = ('user', 'post', 'updated', 'created')