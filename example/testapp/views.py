from django.http import HttpResponse
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages

import io

def home(request):
    return render(request, "index.html")

def send_test_email(request):
    """Send a test email to see it in the debug toolbar mail panel"""
    send_mail(
        'Test Email Subject',
        'This is a test email body to check the mail panel.',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )
    messages.success(request, "A test email has been sent.")
    return redirect("home")


def send_test_attachment(request):
    """Send a test email to see it in the debug toolbar mail panel"""
    email = EmailMessage(
        subject='Test Email Subject',
        body='This is a test email body to check the mail panel.',
        from_email='from@example.com',
        to=['to@example.com'],
    )
    # Create content in memory
    content = "This is generated content\nLine 2\nLine 3"
    email.attach('generated_file.txt', content, 'text/plain')
    email.send()

    messages.success(request, "A test email and attachment has been sent.")
    return redirect("home")


