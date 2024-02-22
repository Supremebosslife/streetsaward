from django.core.mail import send_mail

# Example function for sending registration confirmation email
def send_registration_email(user_email):
    send_mail(
        'Registration Confirmation',
        'Thank you for registering!',
        'mail@streetsaward.com',  # Sender email address
        [user_email],  # List of recipient email addresses (dynamic)
        fail_silently=False,
    )

# Example function for sending password recovery email
def send_password_recovery_email(user_email):
    send_mail(
        'Password Recovery',
        'Here is your password recovery link...',
        'mail@streetsaward.com',  # Sender email address
        [user_email],  # List of recipient email addresses (dynamic)
        fail_silently=False,
    )
