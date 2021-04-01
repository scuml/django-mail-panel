from django.conf.urls import url
from .views import (
    load_message, display_multipart, download_attachment, clear_message, clear_all_messages
)

_PREFIX = 'mail_toolbar'

urlpatterns = [
    url(
        r'^{0}/load_message/(?P<message_id>[\w]+)/$'.format(_PREFIX),
        load_message,
        name="load_message"
    ),
    url(
        r'^{0}/download_attachment/(?P<message_id>[\w]+)/(?P<attachment_id>[\d]+)/$'.format(_PREFIX),
        download_attachment,
        name="download_attachment"
    ),
    url(
        r'^{0}/display_multipart/(?P<message_id>[\w]+)/(?P<multipart>[\w/]+)$'.format(_PREFIX),
        display_multipart,
        name="display_multipart"
    ),

    url(
        r'^{0}/clear_message/(?P<message_id>[\w]+)/$'.format(_PREFIX),
        clear_message,
        name="clear_message"
    ),
    url(
        r'^{0}/clear_all_messages/$'.format(_PREFIX),
        clear_all_messages,
        name="clear_all_messages"
    ),
]
