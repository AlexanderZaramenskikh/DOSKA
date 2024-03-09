from django import forms
from .models import Post
from datetime import date
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'choice', 'author']
        widgets = {
            'time_create': forms.DateInput(attrs={'type': 'date'}),
        }
