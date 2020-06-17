from django.core import mail

def send_email(sender, recipient, subject, content, test=False):
        with mail.get_connection() as connection:
            mail.EmailMessage(
                subject, content, sender, recipient,
                connection=connection
            ).send()

# needs test / logger info like:
"""     def send_email(self, sender, recipient, subject, content, test=False):
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