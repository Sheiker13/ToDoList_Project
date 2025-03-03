from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_task_notification(email, task_title):
    send_mail(
        'Новая задача!',
        f'Вам назначена задача: {task_title}',
        'admin@todo.com',
        [email],
        fail_silently=False,
    )
