from django.urls import include, path, re_path

from . import views

mail_toolbar_patterns = [
    path("load_message/<slug:message_id>/", views.load_message, name="load_message"),
    path(
        "download_attachment/<slug:message_id>/<int:attachment_id>/",
        views.download_attachment,
        name="download_attachment",
    ),
    re_path(
        r"^display_multipart/(?P<message_id>[\w]+)/(?P<multipart>[\w/]+)$",
        views.display_multipart,
        name="display_multipart",
    ),
    path("clear_message/<slug:message_id>/", views.clear_message, name="clear_message"),
    path("clear_all_messages/", views.clear_all_messages, name="clear_all_messages"),
]

urlpatterns = [
    path("mail_toolbar/", include(mail_toolbar_patterns)),
]
