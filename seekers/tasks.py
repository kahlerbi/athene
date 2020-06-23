from __future__ import absolute_import, unicode_literals

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from celery import shared_task

@shared_task
def print_task():
    logger.info('Task Succeeded')
    return 'Task Succeeded'