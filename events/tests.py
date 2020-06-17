from django.test import TestCase
from django.core import mail
import base64
import datetime
from email.mime.text import MIMEText
from email import encoders
import json
import logging
import os
import pickle

# Create your tests here.

class EmailTestCase(TestCase):
    def test_send_email(self, sender='postmaster@sandboxd8e83a2acbd844bbbbca06fde883de7b.mailgun.org', recipient=['shaun.kahler@gmail.com'], subject='test', content='success test'):
        #message = MIMEText(content)
        #payload = {'raw': base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode('ascii')}
        with mail.get_connection() as connection:
            mail.EmailMessage(
                subject, content, sender, recipient,
                connection=connection,
            ).send()

    """ def send_email(self, sender, recipient, subject, content, test=False):
        message = MIMEText(content)
        message['to'] = recipient
        message['from'] = sender
        message['subject'] = subject
        payload = {'raw': base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode('ascii')}
        try:
            logger.info('Sending email to %s', recipient)
            if test:
                logger.debug('%s', content)
            else:
                self.service.users().messages().send(userId='me', body=payload).execute()
        except errors.HttpError as e:
            logger.exception('Error communicating with Gmail!') """