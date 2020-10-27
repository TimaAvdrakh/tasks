from django.core.signals import request_finished
from django.dispatch import receiver
from .models import Notification
from django.db.models.signals import post_save
from .tasks import send_email

@receiver(post_save, sender=Notification)
def my_callback(sender, instance ,**kwargs):
    content = instance.content
    users = instance.users
    emails= []
    for user in users:
        if user.email:
            emails.append(user.email)

    send_email.apply_async(kwargs={'content': content, 'emails': emails})

