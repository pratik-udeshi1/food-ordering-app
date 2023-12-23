import logging

from celery import shared_task
from django.core.mail import send_mail

logging.basicConfig(filename='celery_tasks.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)


@shared_task
def send_order_status_email():
    subject = 'Order Status Update'
    message = f'Your order with ID 123456 has been updated to testing.'
    from_email = 'you@example.com'
    recipient_list = ['customer@example.com']

    send_mail(subject, message, from_email, recipient_list)
    logger.info(f"Email sent for order zzzz with status ddddddd")
    return True