from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from django.conf import settings

from .models import Post, Subscriber


@shared_task
def send_message_after_add_post(pk):
    post = Post.objects.get(id=pk)
    categories = set(post.category.all())
    emails = set(
        Subscriber.objects.filter(category__category_name__in=categories).values_list('user__email', flat=True))

    subject = f'Новый пост в категории {[i for i in categories]}'

    text_content = (
        f'Заголовок: {post.heading}\n'
        f'{post.preview()}\n\n'
        f'Ссылка на пост: http://127.0.0.1:8000{post.get_absolute_url()}'
    )
    html_content = (
        f'<h2> Заголовок: {post.heading} </h2><br>'
        f'{post.preview()}<br><br>'
        f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">Ссылка на пост</a>'
    )

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def weekly_send_message():
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    posts = Post.objects.filter(add_time__gte=week_ago)
    categories = set(posts.values_list('category__category_name', flat=True))
    subscribers = set(
        Subscriber.objects.filter(category__category_name__in=categories).values_list('user__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts
        }
    )

    msg = EmailMultiAlternatives(
        subject="Новые статьи за неделю",
        body='',
        from_email=None,
        to=subscribers)

    msg.attach_alternative(html_content, "text/html")
    msg.send()

# команда запуска: celery -A NewsPortal worker -l INFO --pool=solo
# команда запуска: celery -A NewsPortal beat -l INFO
