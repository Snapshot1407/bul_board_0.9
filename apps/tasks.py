from celery import shared_task
from time import sleep
import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post


@shared_task
def send_email_task(slug):
    post = Post.objects.get(slug=slug)
    categories = post.categories.all()
    title = post.title
    subscribers_email = []

    for c in categories:
        subscribers_user = c.subscribers.all()
        for s_u in subscribers_user:
            subscribers_email.append(s_u.email)

    html_content = render_to_string(
        'subscribe/post_created.html',
        {
            'text': post.preview,
            'link': f'http://127.0.0.1:8000/ru/{slug}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
