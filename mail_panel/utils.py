from django.core.cache import caches
from django.core.mail import EmailMultiAlternatives

try:
    CACHE_SETTINGS = caches.settings
except AttributeError:  # < Django 3.2
    from django.conf import settings

    CACHE_SETTINGS = settings.CACHES

from .conf import MAIL_TOOLBAR_CACHE_KEY, MAIL_TOOLBAR_TTL

# Use local memory cache if default cache is a DummyCache
if not CACHE_SETTINGS.get("default", {}).get("BACKEND", "").endswith(".DummyCache"):
    from django.core.cache import cache
else:
    CACHE_SETTINGS["mail_panel"] = {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "mail-panel",
    }
    cache = caches.create_connection("mail_panel")


def serialize_email(email):
    """
    Serialize email to a dictionary (prior to caching).
    """
    return {
        "subject": email.subject,
        "body": email.body,
        "from_email": email.from_email,
        "to": email.to,
        "cc": email.cc,
        "bcc": email.bcc,
        "headers": email.extra_headers,
        "alternatives": email.alternatives,
    }


def deserialize_email(message_id, data):
    """
    Deserialize a dictionary representing an email (after getting it from the cache).
    """
    from .backend import MailToolbarBackendEmail

    django_email = EmailMultiAlternatives(
        subject=data["subject"],
        body=data["body"],
        from_email=data["from_email"],
        to=data["to"],
        cc=data.get("cc", []),
        bcc=data.get("bcc", []),
        headers=data.get("headers", {}),
    )
    email = MailToolbarBackendEmail(django_email, id=message_id)
    for alt in data.get("alternatives", []):
        email.attach_alternative(alt[0], alt[1])
    return email


def load_outbox():
    """
    Returns a dictionary of cached mail.
    """
    # Since the emails in the cache are serialized, we first deserialize them.
    outbox_obj_of_serialized_emails = cache.get(MAIL_TOOLBAR_CACHE_KEY, {})
    outbox = {}
    for email_id, serialized_email in outbox_obj_of_serialized_emails.items():
        email = deserialize_email(email_id, serialized_email)
        outbox[email_id] = email
    return outbox


def save_outbox(outbox):
    """
    Saves the dictionary of cached mail and sets expiry.
    """
    outbox_obj = {}
    # Since some emails contain data types that can not be serialized, we first
    # serialize emails to a serializable object.
    for email_id, email in outbox.items():
        outbox_obj[email_id] = serialize_email(email)

    cache.set(MAIL_TOOLBAR_CACHE_KEY, outbox_obj, MAIL_TOOLBAR_TTL)


def clear_outbox():
    """
    Utility function to clear the dictionary of cached mail. Typical use case: Starting a new real-human test session.
    """
    cache.set(MAIL_TOOLBAR_CACHE_KEY, {})
