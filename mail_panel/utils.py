from django.core.cache import caches

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


def load_outbox():
    """
    Returns a dictionary of cached mail.
    """
    return cache.get(MAIL_TOOLBAR_CACHE_KEY, {})


def save_outbox(outbox):
    """
    Saves the dictionary of cached mail and sets expiry.
    """
    cache.set(MAIL_TOOLBAR_CACHE_KEY, outbox, MAIL_TOOLBAR_TTL)


def clear_outbox():
    """
    Utility function to clear the dictionary of cached mail. Typical use case: Starting a new real-human test session.
    """
    cache.set(MAIL_TOOLBAR_CACHE_KEY, {})
