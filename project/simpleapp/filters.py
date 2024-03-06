from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Post
from django import forms
from django.contrib.auth.models import User
from django.db.models.query import QuerySet


class PostFilter(FilterSet):
    start_date = DateFilter(
        field_name='time_create',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата публикации, с'
    )
    end_date = DateFilter(
        field_name='time_create',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата публикации, до'
    )
    title = CharFilter(lookup_expr='icontains', label='Заголовок')

    class Meta:
        model = Post
        fields = {
            'author': ['exact'],
        }

