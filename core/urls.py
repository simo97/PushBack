from django.urls import path
from .views import testpage


app_name = 'core'


urlpatterns = [
    path('testpage/', testpage, name='test_ws'),
]