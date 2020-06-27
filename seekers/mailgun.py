from django.core import mail

def send_email(sender, recipient, subject, content, test=False):
        with mail.get_connection() as connection:
            mail.EmailMessage(
                subject, content, sender, recipient,
                connection=connection
            ).send()