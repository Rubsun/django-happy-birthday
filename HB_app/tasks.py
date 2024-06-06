from os import getenv

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from dotenv import load_dotenv

from .models import Subscription, Client

load_dotenv()


@shared_task
def send_birthday_notifications():
    """
    Send birthday notifications to clients at their specified notification time.
    """
    now = timezone.now().time()
    today = timezone.now().date()

    clients_to_notify = Client.objects.filter(notification_time__hour=now.hour, notification_time__minute=now.minute)

    for client in clients_to_notify:
        subscriptions = Subscription.objects.filter(user=client, subscribed_to__date_of_birth=today)

        for subscription in subscriptions:
            subscribed_to = subscription.subscribed_to
            subject = f"Happy Birthday to {subscribed_to.first_name} {subscribed_to.last_name}!"
            message = f"Dear {client.first_name},\n\nToday is {subscribed_to.first_name} {subscribed_to.last_name}'s birthday. Don't forget to send your wishes!"
            recipient_list = [client.email]
            send_mail(subject, message, recipient_list=recipient_list, from_email=getenv('EMAIL_HOST_USER'),
                      auth_password=getenv('EMAIL_HOST_PASSWORD'))
