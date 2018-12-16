from django.contrib import admin
from .models import *
# Register your models here.


class ApplicationModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'app_token')


class ClientModeAdmin(admin.ModelAdmin):
    list_display = ('app', 'client_id', 'currently_connected', 'last_connection')
    list_filter = ('app',)


class NotificationModelAdmin(admin.ModelAdmin):
    list_display = ('internal_uuid', 'content')


admin.site.register(Application, ApplicationModelAdmin)
admin.site.register(Notification, NotificationModelAdmin)
admin.site.register(Client, ClientModeAdmin)
