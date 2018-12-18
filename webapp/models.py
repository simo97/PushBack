from django.db import models
from django.conf.global_settings import AUTH_USER_MODEL
from django.utils.translation import gettext as _

# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', verbose_name=_('User avatar'))

    def __str__(self):
        return '{}\'s account'.format(self.user.username)

