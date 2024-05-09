__version__ = '4.0.4'

# Monkey patch the PANELS_DEFAULTS to add mail panel
try:
    from debug_toolbar import settings

    try:
        log_index = settings.PANELS_DEFAULTS.index("debug_toolbar.panels.logging.LoggingPanel")
        settings.PANELS_DEFAULTS.insert(log_index, 'mail_panel.panels.MailToolbarPanel')
    except ValueError:
        settings.PANELS_DEFAULTS.append('mail_panel.panels.MailToolbarPanel')
except ImportError:
    pass
