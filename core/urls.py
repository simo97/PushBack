from django.urls import path
from .views import register_users, notify, testpage


app_name = 'api'


urlpatterns = [
    path('register/', register_users, name='register_user'),
    path('notify/', notify, name='notify_user'),
    path('testpage/', testpage, name='test_ws'),

]