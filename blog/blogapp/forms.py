# blog/forms.py
from django import forms
from .models import Post, Comment, Rating


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields: list[str] = ['title', 'content', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields: list[str] = ['content']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields: list[str] = ['value']


class SearchForm(forms.Form):
    query = forms.CharField(required=False)