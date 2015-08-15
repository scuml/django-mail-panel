from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from django.views.static import serve
from django.utils.html import urlize
from django.utils.safestring import mark_safe

import os
from utils import load_outbox, save_outbox

if hasattr(settings, "DEBUG_TOOLBAR_FILTER_URL"):
    settings.DEBUG_TOOLBAR_FILTER_URL = settings.DEBUG_TOOLBAR_FILTER_URL + ("__mail_toolbar_debug__")
else:
    settings.DEBUG_TOOLBAR_FILTER_URL = ("__mail_toolbar_debug__",)

def load_message(request, message_id):
    """
    Loads a message template into the subframe
    """
    message = None
    mail_list = load_outbox()
    if mail_list:
        message = mail_list.get(message_id)

    alternatives = list()
    if message:
        if message.read is False:
            message.read = True

        save_outbox(mail_list)

        if message.body:
            alternatives.append("text/plain")
        for alternative in message.alternatives:
            alternatives.append(alternative[1])

    return render(request, 'django_mail_toolbar/message_overview.html', dict(
        message=message,
        alternatives=alternatives,
    ))


def display_multipart(request, message_id, multipart):
    mail_list = load_outbox()
    message = mail_list.get(message_id)
    if multipart not in ('', 'text/plain'):
        for alternative in message.alternatives:
            if alternative[1] == multipart:
                body = mark_safe(alternative[0].replace("<a ", "<a target='_blank'"))
                return HttpResponse(body)


    return render(request, "django_mail_toolbar/plain_text_message.html", dict(
        body=mark_safe(
            urlize(message.body).replace("<a ", "<a target='_blank'"))
    ))


def download_attachment(request, message_id, attachment_id):
    """
    Downloads an attachment from a message
    """

    mail_list = load_outbox()
    message = mail_list.get(message_id)
    attachment = message.attachments[int(attachment_id)]

    response = HttpResponse(attachment[1])
    # Force download as attachment
    response['Content-Type'] = ''
    if attachment[2]:
        response['Content-Type'] = attachment[2]


    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        attachment[0]
    )

    return response

def serve_static(request, path):
    """View to serve static assets"""
    root = getattr(settings, 'MAIL_TOOLBAR_MEDIA_ROOT', None)
    if root is None:
        parent = os.path.abspath(os.path.dirname(__file__))
        root = os.path.join(parent, 'static', 'mail_toolbar')
    return serve(request, path, root)
