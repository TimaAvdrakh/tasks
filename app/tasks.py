from __future__ import absolute_import, unicode_literals

from celery import shared_task
from datetime import datetime

from django.core.mail import send_mail
from .models import Task

@shared_task
def add(x, y):
    return x + y

# @shared_task
# def check_for_orders():
#     # orders = Order.objects.all()
#     # now = datetime.datetime.utcnow().replace(tzinfo=utc,second=00, microsecond=00)
#     # week_old = now - datetime.timedelta(week=1)
#     # for order in orders:
#     #     if order.manu_date.date() == week_old.date():
#     #         send_mail('Manufacturing Reminder',
#                 '{{Order.id}} is due {{manu_date}}',
#                 'dummyguy1680@gmail.com',
#                 ['gummy@gmail.com.com'])
#             return None

@shared_task
def send_email(**kwargs):
    send_mail(
        'Subject here',
        kwargs['content'],
        'from@example.com',
        kwargs['emails'],
        fail_silently=False,
    )

@shared_task()
def daily_deadline_reports():
    tasks = Task.objects.all()
    today = datetime.now().date()
    print(today)
    overdue_tasks = tasks.filter(deadline__lte=today)
    if not overdue_tasks.exists():
        return 0

    for task in overdue_tasks:
        executor = task.executor
        send_email(
            "OUT of Deadline ",
            f"Deadline for task {task.name} overdue",
            'from@example.com',
            executor.email,
            fail_silently=False
        )
