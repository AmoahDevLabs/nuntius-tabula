from datetime import datetime

from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from core.models import MessageBoard


@shared_task(name='email_notification')
def send_email_task(subject, body, email_address):
    email = EmailMessage(subject, body, to=[email_address])
    email.send()
    return email_address


@shared_task(name='monthly_newsletter')
def send_newsletter_task():
    subject = 'Monthly Newsletter Letter'
    subscribers = MessageBoard.objects.get(id=2).subscribers.filter(profile__newsletter_subscribed=True)
    for subscriber in subscribers:
        body = render_to_string('core/news_letter.html', {'name': subscriber.profile.name})
        email = EmailMessage(subject, body, to=[subscriber.email])
        email.content_subtype = 'html'
        email.send()
    current_month = datetime.now().strftime('%B')
    subscriber_count = subscribers.count()
    return f'{current_month} Newsletter Letter to {subscriber_count} subscribers'
