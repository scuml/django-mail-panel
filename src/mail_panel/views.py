from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.utils.html import urlize
from django.utils.safestring import mark_safe

from .utils import load_outbox, save_outbox, clear_outbox

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
    message = mail_list.get(message_id, None)

    alternatives = list()
    if message:
        message.read = True

        save_outbox(mail_list)

        if message.body:
            if hasattr(message, 'content_subtype') and message.content_subtype == "html":
                alternatives.append("text/html")
            else:
                alternatives.append("text/plain")
        if hasattr(message, "alternatives"):
            for alternative in message.alternatives:
                alternatives.append(alternative[1])

    return render(request, 'mail_panel/message_overview.html', dict(
        message=message,
        alternatives=alternatives,
    ))


def display_multipart(request, message_id, multipart):
    """
    Displays the requested multipart from the email message.
    """

    mail_list = load_outbox()
    message = mail_list.get(message_id, None)
    if not message:
        return HttpResponse('Messsage has expired from cache.')

    if multipart not in ('', 'text/plain'):
        if hasattr(message, "alternatives"):
            for alternative in message.alternatives:
                if alternative[1] == multipart:
                    body = mark_safe(alternative[0].replace("<a ", "<a target='_blank'"))
                    return HttpResponse(body)
        else:
            body = mark_safe(message.body.replace("<a ", "<a target='_blank'"))
            return HttpResponse(body)


    return render(request, "mail_panel/plain_text_message.html", dict(
        body=mark_safe(
            urlize(message.body).replace("<a ", "<a target='_blank'"))
    ))


def download_attachment(request, message_id, attachment_id):
    """
    Downloads an attachment from a message
    """

    mail_list = load_outbox()
    message = mail_list.get(message_id, None)
    if not message:
        return HttpResponse('Messsage has expired from cache.')

    filename, content, content_type = message.attachments[int(attachment_id)]
    response = HttpResponse(content)

    if content_type:
        response['Content-Type'] = content_type

    # Force download as attachment
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        filename
    )

    return response

def clear_message(request, message_id):
    """
    Clears a message from the cache
    """
    mail_list = load_outbox()
    try:
        del(mail_list[message_id])
    except KeyError:
        pass
    save_outbox(mail_list)

    return JsonResponse({"status": "success"})

def clear_all_messages(request):
    """
    Clears all message from the cache
    """
    clear_outbox()

    return JsonResponse({"status": "success"})
