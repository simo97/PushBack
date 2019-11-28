from django.urls import path

from .views import RegistrationView, NotifyView

app_name = 'api'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register_users'),
    path('notify/', NotifyView.as_view(), name='notify_users'),
]
