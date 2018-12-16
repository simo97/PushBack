from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from channels.db import database_sync_to_async
from .models import Client, Application
import json


"""
naming convention here

INTERNAL_ID + CHANNEL_NAME channel name key in cache
INTERNAL_ID + STATUS client status in the cache
"""


class NotificationConsumer(AsyncWebsocketConsumer):
    _client_channel_name = ''
    _client_conn_status = ''
    _client_obj = None

    def get_client_from_db(self, app_id, user_id):
        return Client.objects.filter(app=Application.objects.get(app_token=app_id), client_id=user_id).first()

    async def connect(self):
        """
        define the status (available/not) in the cache here, t should come with the :app and :user_id from
        the app db
        :return:
        """
        clt = await database_sync_to_async(self.get_client_from_db)(
            self.scope['url_route']['kwargs']['app_id'],
            self.scope['url_route']['kwargs']['client_id'],
        )
        if clt is not None:
            self._client_obj = clt
            self._client_channel_name = '{}_CHANNEL_NAME'.format(clt.current_connection_id)
            self._client_conn_status = '{}_CHANNEL_CONNECTION_STATUS'.format(clt.current_connection_id)
            cache.set(self._client_channel_name, self.channel_name)
            cache.set(self._client_conn_status, True)

            print(self._client_channel_name, ' channel name in the connect')

        await self.accept()

    async def disconnect(self, code):
        """
        Unset the availability in the cache
        :param code:
        :return:
        """
        cache.delete_many([self._client_channel_name, self._client_conn_status])

    async def send_notification(self, event):
        """
        Send notification to one client
        :param event:
        :return:
        """
        print(event, ' ==== les events ici ==== ')
        await self.send(text_data=event['content'])
