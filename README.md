
## Django Debug Toolbar - Mail Panel

[![Build Status](https://secure.travis-ci.org/scuml/django-mail-panel.png?branch=master)](http://travis-ci.org/scuml/django-mail-panel)

![](https://cloud.githubusercontent.com/assets/1790447/9289964/6aa7c4ba-434e-11e5-8594-3bb3efd0cd81.png)


Testing and debugging e-mail while developing a Django app has never been pleasant.  Sending e-mail to a file-based backend requires a user to click through obtusely-named files and does not provide a way to preview rendered HTML.  Sending e-mail to a valid mailbox incurs a delay as the message is processed though a mail server, and clutters a developer's inbox.

The mail panel attempts to address these problems by providing a way to preview emails within the browser using [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar).

This mail panel is released under the Apache license. If you like it, please consider contributing!

Special thanks to @ShawnMilo for the code review.


Installation
============

To install the mail panel, first install this package with `pip install django-mail-panel`.  Then add the `mail_panel` app after `debug_toolbar`to the `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = (
    ...
    'debug_toolbar',
    'mail_panel',
)
```

and add the panel `DEBUG_TOOLBAR_PANELS`:

```python
DEBUG_TOOLBAR_PANELS = (
    ...
    'mail_panel.panels.MailToolbarPanel',
)
```


Collect static and you'll be good to go.

```bash
./manage.py collectstatic
```


Configuration
=============

After installation, you now need to redirect mail to the mail toolbar.  Change your email backend to the following:

```python
EMAIL_BACKEND = 'mail_panel.backend.MailToolbarBackend'
```

**Important:** This plugin uses Django's cache backend to store messages.  If you are using `DummyCache`, the mail panel will use a local memory cache, and will reset messages when the server is restarted.


**[Optional]** 
By default, mail toolbar stores messages for one day before removing them from cache.  You can change this with the following setting:

```python
MAIL_TOOLBAR_TTL = 86400  # 1 Day
```

**[Optional]**
If you use the `DEBUG_TOOLBAR_PANELS` to custom order your panels:

```python
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
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'mail_panel.panels.MailToolbarPanel',
    ]
```



Testing
=======

To preview emails sent from your test suite, add the email backend override to your tests with the following:

```python
from django.test.utils import override_settings

@override_settings(EMAIL_BACKEND='mail_panel.backend.MailToolbarBackend')
def test_send_email(self):
    # your code here
```


The backend works similarly to the standard email backend and code should not need to be reworked when using the MailToolbarBackend.


```python
from django.core import mail

original_outbox = len(mail.outbox)
# Send mail ...
assert(len(mail.outbox) == original_outbox + 1)
```

Shameless Plugs
=======
Like Django Mail Panel?  Be sure to check out and support these other tools for Mac that will improve your workflow:

**[Kubermagic](https://echodot.com/kubermagic/)** - Automate, and script away tedious kubectl commands with Kubermagic; a UI for developers, QA teams, and those starting to learn the ins-and-outs of Kubernetes.     


**[Red](https://echodot.com/red/)** - A visual and interactive Redis client, featuring live updating keys, an interactive console, pub/sub, lua script support and much more.
