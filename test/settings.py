SECRET_KEY = "test"
DEBUG = True
ROOT_URLCONF = "urls"

INSTALLED_APPS = (
    "debug_toolbar",
    "mail_panel",
)
DEBUG_TOOLBAR_PANELS = [
    "mail_panel.panels.MailToolbarPanel",
]
