from django.conf.urls import url

from . import consumer

websocket_urlpatterns = [
    url(r'^ws/notifications/subscribe/(?P<app_id>[^/]+)/(?P<client_id>[^/]+)/$', consumer.NotificationConsumer),
]