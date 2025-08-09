from django.utils.translation import gettext_lazy as _

from collections import OrderedDict
import datetime

from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils.timezone import now

from debug_toolbar.panels import Panel

from .conf import MAIL_TOOLBAR_TTL
from .utils import load_outbox, save_outbox
from .urls import urlpatterns


class MailToolbarPanel(Panel):
    """
    Panel that displays informations about mail
    """
    name = 'Mail'
    template = 'mail_panel/panel.html'
    has_content = True
    is_historical = False
    is_async = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def scripts(self):
        scripts = super().scripts
        scripts.append(static("debug_toolbar/mail/toolbar.mail.js"))
        return scripts

    @property
    def nav_subtitle(self):
        mail_list = load_outbox()
        unread_count = 0
        for message in list(mail_list.values()):
            if not message.read:
                unread_count += 1
        if unread_count == 1:
            return '{0} unread message'.format(unread_count)
        elif unread_count > 1:
            return '{0} unread messages'.format(unread_count)
        return ''

    @property
    def title(self):
        return _('Mail')

    def get_stats(self):
        return self.generate_stats()

    @property
    def content(self):
        mail_list = self.get_mail_list()
        self.record_stats({"mail_list": mail_list})
        return render_to_string('mail_panel/panel.html', {
            "mail_list": mail_list
        })

    def get_mail_list(self):
        """
        Main panel view.  Loads and displays listing of mail.
        """
        mail_list = load_outbox()

        # Return empty mail list early if nothing there.
        if mail_list == {}:
            return mail_list

        mail_list = OrderedDict(
            sorted(iter(mail_list.items()),
            key=lambda x: x[1].date_sent,
            reverse=True
        ))
        prev_len = len(mail_list)

        # Expire messages past TTL
        expire_at = now() - datetime.timedelta(
            seconds=MAIL_TOOLBAR_TTL)

        for message_id, message in list(mail_list.items()):
            if message.date_sent < expire_at:
                del mail_list[message_id]

        if prev_len != len(mail_list):
            save_outbox(mail_list)

        return mail_list

    def generate_stats(self, request, response):
        # Need dummy info here to record data
        # Mail is handled globally and not per-request.
        self.record_stats({"a":"1"})

    @classmethod
    def get_urls(cls):
        return urlpatterns
