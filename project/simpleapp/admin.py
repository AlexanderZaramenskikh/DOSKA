from django.contrib import admin
from .models import Category, Post


def nullfy_quantity(modeladmin, request,queryset):
    queryset.update(post_rating=0)
nullfy_quantity.short_description = 'Сбросить рейтинг'


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'post_rating')
    list_filter = ('title', 'category', 'time_create')
    search_fields = ('title', 'category')
    actions = [nullfy_quantity]


admin.site.register(Category)
admin.site.register(Post, PostAdmin)