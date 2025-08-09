from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('send-email/', views.send_test_email, name='send_test_email'),
    path('send-attachment/', views.send_test_attachment, name='send_test_attachment'),
]
