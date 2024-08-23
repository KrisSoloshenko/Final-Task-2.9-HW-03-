from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from .tasks import send_message_after_add_post


@receiver(m2m_changed, sender=PostCategory)
def post_category_created(instance, **kwargs):
    if not kwargs['action'] == 'post_add':
        return

    send_message_after_add_post.delay(instance.id)
