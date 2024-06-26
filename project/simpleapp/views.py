import datetime
from datetime import date

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, mail_managers, send_mail
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.views import TemplateView

from .models import Post, Category, Author, UserCategory
from .filters import PostFilter
from .forms import PostForm
from django.db.models.signals import post_save
from django.http import HttpResponse
from django.views import View
from django.core.cache import cache

class NewsList(ListView):
    model = Post
    ordering = 'time_create'

    # queryset = Post.objects.order_by('time_create')

    template_name = 'news.html'
    context_object_name = 'News'
    paginate_by = 5

    def get_queryset(self):
        # self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(choice='NE').order_by('-time_create')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        # context['category'] = self.category

        return context


class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'Search'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'a_news.html'
    context_object_name = 'A_news'


class ArticleList(ListView):
    model = Post
    ordering = 'date'
    template_name = 'articles.html'
    context_object_name = 'Articles'

    def get_queryset(self):
        queryset = Post.objects.filter(choice='AR').order_by('-time_create')
        return queryset


class ArticleDetail(DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'Article'
    queryset = Post.objects.filter(choice='AR')

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'article-{self.kwargs["pk"]}',None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'article-{self.kwargs["pk"]}', obj)

        return obj


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        today = datetime.date.today()
        post_limit = Post.objects.filter(author=post.author, time_create__date=today).count()
        if post_limit >= 3:
            return render(self.request, 'to_many_post.html', {'author': post.author})
        post.save()
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.add_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.delete_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.choice = 'AR'
        return super().form_valid(form)


class ArticleEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class CategoryListView(NewsList):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    UserCategory.objects.create(category=category, user=user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})


def to_many_post(request):
    return render(request, 'news/to_many_post.html')

class HomeView(TemplateView):
    template_name = 'home.html'
