from __future__ import absolute_import, unicode_literals

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

import seekers.mailgun
from django.core import mail

from celery import shared_task

@shared_task
def print_task():
    logger.info('Task Succeeded')
    return 'Task Succeeded'

@shared_task
def send_email(sender, recipient, subject, content, test=False):
    print('email task deployed')
    with mail.get_connection() as connection:
        mail.EmailMessage(
            subject, content, sender, recipient,
            connection=connection
        ).send()