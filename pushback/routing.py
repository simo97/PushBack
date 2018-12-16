from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf.urls import url
from core.consumer import NotificationConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter([
            url(r'^ws/notifications/subscribe/(?P<app_id>\w+)/(?P<client_id>\w+)/$', NotificationConsumer)
        ])
    )
})
