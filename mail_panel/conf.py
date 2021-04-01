from django.conf import settings

MAIL_TOOLBAR_TTL = getattr(settings, 'MAIL_TOOLBAR_TTL', 86400)
MAIL_TOOLBAR_CACHE_KEY = 'mail_toolbar_outbox'
