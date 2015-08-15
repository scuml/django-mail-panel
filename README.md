
Django Debug Toolbar - Mail Panel
===============================

Testing and debugging emails while developing a django app has never been pleasant.  Sending emails to a file-based backend requires a user to click through obtusely named files and does not provide a way to preview rendered html.  Sending email to a valid mailbox incurs a delay as the email is processed though a mail server, all the while adding clutter to a developer's inbox, and even occasionally finds itself buried in a spam directory.

The Django Debug Toolbar Mail Panel attempts to address these problems by providing a way to preview emails within the browser window.

This Django Debug Toolbar panel is released under the BSD license, like Django
and the Django Debug Toolbar. If you like it, please consider contributing!

The debug toolbar mail panel was originally created by Stephen Mitchell
in August 2015 for The Tracktor.


Installation
============

To install the mail panel, first install this package with `pip install django-debug-toolbar-mail`, then add debug_toolbar_mail after debug_toolbar to INSTALLED_APPS setting:

    INSTALLED_APPS = (
        ...
        'debug_toolbar',
        'debug_toolbar_mail',
    )

and add the panel DEBUG_TOOLBAR_PANELS:

    DEBUG_TOOLBAR_PANELS = (
        ...
        'debug_toolbar_mail.panels.MailToolbarPanel',
    )


If you don't yet have the setting, you can append and reorder your panels wiht this:

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar_mail.panels.MailToolbarPanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]


Collect static and you'll be good to go.

    ./manage.py collectstatic


Configuration
=============

After installation, you now need to redirect mail to the mail toolbar.  Change your email backend to the following:

    EMAIL_BACKEND = 'debug_toolbar_mail.backend.MailToolbarBackend'


By default, mail toolbar stores messages for one day before removing them from cache.  You can change this with the following setting:

    MAIL_TOOLBAR_TTL = 86400  # 1 Day

Testing
=======

To preview emails sent from your test suite, add the email backend override to your tests with the following:
from django.test.utils import override_settings

    @override_settings(EMAIL_BACKEND='debug_toolbar_mail.backend.MailToolbarBackend')
    def test_send_email(self):
        ...

