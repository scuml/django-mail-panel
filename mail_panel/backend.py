from django.core import mail
from django.core.mail.backends.locmem import EmailBackend
from django.utils.timezone import now
import datetime
from uuid import uuid4

from .utils import load_outbox, save_outbox


class MailToolbarBackendEmail(mail.EmailMultiAlternatives):
    def __init__(self, message):
        self.id = uuid4().hex
        self.date_sent = now()
        self.read = False
        message.message()  # triggers header validation

        alternatives = getattr(message, "alternatives", None)

        super().__init__(
            subject=message.subject,
            to=message.to,
            cc=message.cc,
            bcc=message.bcc,
            reply_to=message.reply_to,
            from_email=message.from_email,
            body=message.body,
            alternatives=alternatives,
            headers=message.extra_headers,
            attachments=message.attachments,
        )


    @property
    def get_subject(self):
        return self.subject

class MailToolbarBackend(EmailBackend):
    """A email backend for use during testing.

    The test connection stores email messages in a dummy outbox,
    rather than sending them out on the wire.  This is cached and
    can be accessed via the memmail interface.

    Also store in LocMem for compatibility with tests.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.outbox = load_outbox()

    def send_messages(self, messages):
        """Redirect messages to the cached outbox"""

        for message in messages:
            new_message = MailToolbarBackendEmail(message)
            self.outbox[new_message.id] = new_message

        save_outbox(self.outbox)

        return super().send_messages(messages)
