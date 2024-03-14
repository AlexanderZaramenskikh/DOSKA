from celery import shared_task
import datetime
from django.utils import timezone
from simpleapp.models import Post, Category, UserCategory
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import UserCategory
from django.contrib.auth.models import User

@shared_task
def send_week():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_create__gte=last_week)
    print(posts)
    categories = set(posts.values_list('category__category_name', flat=True))
    subs = set(Category.objects.filter(category_name__in=categories).values_list('usercategory__user', flat=True))
    valid_subs = set(User.objects.filter(id__in=subs).values_list('email', flat=True))
    print(f'categories - {categories}\n, subs - {subs}\n, valid_subs - {valid_subs}')

    for email in valid_subs:
        sub_idx = User.objects.filter(email=email).first().id
        category_lst = list(UserCategory.objects.filter(user=sub_idx).values_list('category', flat=True))
        print(f'category_lst - {category_lst}')

        for ctg in category_lst:
            valid_posts = list(posts.filter(category=ctg))
            print(f'valid_posts - {valid_posts}')

            html_content = render_to_string(
                'post_week.html',
                {
                    'link': 'http://127.0.01:8000',
                    'posts': posts,

                }
            )

            msg = EmailMultiAlternatives(
                subject='Новости за неделю',
                body='',
                from_email='dadvzhvda@yandex.ru',
                to=[email],
            )

            msg.attach_alternative(html_content, 'text/html')
            msg.send()
    print('Все отправлено')

@shared_task
def new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    title = post.title
    content = post.content()
    subscribers_emails = []
    for category in categories:
        subscribers = category.subscribers.all()
        subscribers_emails += [s.email for s in subscribers]

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': content,
            'link': f"{'http://127.0.01:8000'}/news/{pk}"
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email='dadvzhvda@yandex.ru',
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
