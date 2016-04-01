from django.core.mail.backends.locmem import EmailBackend
import datetime
from uuid import uuid4

from .utils import load_outbox, save_outbox

class MailToolbarBackend(EmailBackend):
    """A email backend for use during testing.

    The test connection stores email messages in a dummy outbox,
    rather than sending them out on the wire.  This is cached and
    can be accessed via the memmail interface.

    Also store in LocMem for compatibility with tests.
    """

    def __init__(self, *args, **kwargs):
        super(MailToolbarBackend, self).__init__(*args, **kwargs)

        self.outbox = load_outbox()


    def send_messages(self, messages):
        """Redirect messages to the cached outbox"""

        for message in messages:
            try:
                message.id = uuid4().get_hex()
            except AttributeError:
                message.id = uuid4().hex  # python 3
            message.date_sent = datetime.datetime.now()
            message.read = False
            message.message()  # triggers header validation
            self.outbox[message.id] = message

        save_outbox(self.outbox)

        return super(MailToolbarBackend, self).send_messages(messages)
