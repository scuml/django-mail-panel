from django.core.cache import cache

from .conf import MAIL_TOOLBAR_CACHE_KEY, MAIL_TOOLBAR_TTL

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
