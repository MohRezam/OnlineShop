from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_otp_email(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    from_email = 'shadmehrihesam@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)