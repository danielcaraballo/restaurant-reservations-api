from django.core.mail import EmailMessage
import threading
import logging

logger = logging.getLogger(__name__)

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        super().__init__()

    def run(self):
        try:
            self.email.send()
        except Exception as e:
            logger.error(f"Error sending email: {e}")

class Util:
    @staticmethod
    def send_email(data):
        try:
            email = EmailMessage(
                subject=data['email_subject'],
                body=data['email_body'],
                to=[data['to_email']]
            )
            EmailThread(email).start()
        except KeyError as e:
            logger.error(f"Missing key in email data: {e}")
        except Exception as e:
            logger.error(f"Error in send_email method: {e}")
