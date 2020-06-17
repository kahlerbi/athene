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

def test_send_email(sender='postmaster@sandboxd8e83a2acbd844bbbbca06fde883de7b.mailgun.org', recipient=['shaun.kahler@gmail.com'], subject='test', content='success test'):
        #message = MIMEText(content)
        #payload = {'raw': base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode('ascii')}
        with mail.get_connection() as connection:
            mail.EmailMessage(
                subject, content, sender, recipient,
                connection=connection,
            ).send()
        print('test ran')