from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def post_category_created(instance, **kwargs):
    if not kwargs['action'] == 'post_add':
        return

    emails = User.objects.filter(subscriptions__category__in=instance.category.all()).values_list('email', flat=True)

    subject = f'Новый пост в категории {instance.category}'

    text_content = (
        f'Заголовок: {instance.heading}\n'
        f'{instance.preview()}\n\n'
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'<h2> Заголовок: {instance.heading} </h2><br>'
        f'{instance.preview()}<br><br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">Ссылка на пост</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
