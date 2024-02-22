# test_email.py

import os
from django.core.mail import send_mail
from django.conf import settings

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StreetsAward.settings')

def send_test_email():
    subject = 'Test Email'
    message = 'This is a test email.'
    sender_email = 'your_sender_email@example.com'
    recipient_email = 'recipient_email@example.com'

    send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)

if __name__ == "__main__":
    # Configure Django settings
    settings.configure()

    # Call the send_test_email function
    send_test_email()
