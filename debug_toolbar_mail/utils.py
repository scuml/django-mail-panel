from django.core.cache import cache

from conf import MAIL_TOOLBAR_CACHE_KEY, MAIL_TOOLBAR_TTL

def load_outbox():
    return cache.get(MAIL_TOOLBAR_CACHE_KEY)

def save_outbox(outbox):
    cache.set(MAIL_TOOLBAR_CACHE_KEY, outbox, MAIL_TOOLBAR_TTL)
