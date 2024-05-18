from celery import shared_task

from .email import send_contact_email_message


@shared_task
def send_contact_email_message_task(subject, email, content, ip, user_id):
    """
    1. Задача обрабатывается в представлении: FeedbackCreateView
    2. Отправка письма из формы обратной связи осуществляется через функцию: send_contact_email_message
    """
    return send_contact_email_message(subject, email, content, ip, user_id)
