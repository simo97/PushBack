from django.db import models
from django.utils.translation import gettext as _
import shortuuid
from django.core.cache import cache
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.dispatch import receiver
# Create your models here.


class Application(models.Model):
    """
    Represent a registered app.

    Notification and Client a link to one app, when created it generate a app_token which should be used
    in any request send to the PushBack server.
    """
    name = models.CharField(max_length=30, verbose_name=_('Nom de l\'application'))  # application
    app_token = models.CharField(max_length=150, editable=False, verbose_name=_("Token d'acces"), null=True,)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.app_token = shortuuid.ShortUUID().random(150)
        return super(Application, self).save(force_insert, force_update, using, update_fields)


class Notification(models.Model):
    """
    Represent one notification, One Notification in related to many clients.

    It store one internal_uuid used as internal_id and a content. That content represent the notification's content
    as it has been sent by the app server, this content should be on a text form (XML, JSON, etc)
    """
    content = models.TextField(verbose_name=_('Contenu de la notification en JSON'))
    received_date = models.DateTimeField(auto_now=True, verbose_name=_('Date a laquelle il est arriver sur le serveur'))
    internal_uuid = models.CharField(verbose_name=_('Identifiant interne'), max_length=50, editable=False)
    clients = models.ManyToManyField('Client')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.internal_uuid = shortuuid.ShortUUID().random(length=50)
        return super(Notification, self).save(force_insert, force_update, using, update_fields)


class Client(models.Model):
    """
    A client is a representation of one user who should receive a notification, more preciselly a user which
    is currently connected and register in the application
    """
    app = models.ForeignKey(Application, on_delete=models.CASCADE,verbose_name=_('application'))
    client_id = models.IntegerField(verbose_name=_('ID in app'), null=True,
                                    help_text=_('Identifiant du client dans la BD du server'))
    currently_connected = models.BooleanField(verbose_name=_('Utilisateur actuellement connecter'),
                                              null=True, default=False)
    current_connection_id = models.CharField(max_length=100, null=True)  # shoulb generated with shortuuid lib
    last_connection = models.DateTimeField(null=True,)

    def __str__(self):
        return self.current_connection_id

    def set_current_id(self):
        self.current_connection_id = shortuuid.ShortUUID().random(100)
        self.save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.current_connection_id = shortuuid.ShortUUID().random(100)
        return super(Client, self).save(force_insert, force_update, using, update_fields)


#  @receiver(post_save, sender=Notification)
def handle_notification(instance, created):
    """
    handle notification sending through ws here.
    1- get list of client related to this notification
    2- get currently connected client from this list
    3- send notifications

    current_connection_id + CHANNEL_NAME
    _client_channel_name = '{}_CHANNEL_NAME'
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    print('SAVED HERE')

    if created:
        import json
        print('NEW', instance.clients)
        for client in instance.clients.all():

            print(cache.get('{}_CHANNEL_CONNECTION_STATUS'.format(client.current_connection_id)), ' cache state')
            if cache.get('{}_CHANNEL_CONNECTION_STATUS'.format(client.current_connection_id)):  # if connected
                print('client ici ', client)
                chn_layer = get_channel_layer()
                async_to_sync(chn_layer.send)(
                    cache.get('{}_CHANNEL_NAME'.format(client.current_connection_id)),
                    {
                        "type": "send.notification",
                        "content": json.dumps(instance.content)
                    }
                )