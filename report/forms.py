from django import forms
from .models import Post, PostImage


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'location', 'description']


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image', 'description']