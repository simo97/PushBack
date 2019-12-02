from rest_framework import serializers

from ..models import Application, Client, Notification, handle_notification


class RegistrationSerializer(serializers.ModelSerializer):
    app_token = serializers.SlugRelatedField(slug_field='app_token', queryset=Application.objects.all())
    users = serializers.ListField(child=serializers.CharField(), required=True, min_length=1)

    class Meta:
        model = Client
        fields = ('app_token', 'users')

    def create(self, validated_data):
        for user in validated_data['users']:
            Client.objects.get_or_create(client_id=user, app=validated_data['app_token'])


class NotifySerializer(serializers.ModelSerializer):
    app_token = serializers.SlugRelatedField(slug_field='app_token', queryset=Application.objects.all())
    users = serializers.SlugRelatedField(slug_field='client_id', queryset=Client.objects.all(), many=True)
    content = serializers.JSONField(required=True)

    class Meta:
        model = Client
        fields = ('app_token', 'users', 'content')

    def validate(self, validated_data):
        client_ids = [client.pk for client in validated_data['users']]
        validated_data['users'] = Client.objects.filter(client_id__in=client_ids, app=validated_data['app_token'])
        return validated_data

    def create(self, validated_data):
        notification = Notification.objects.create(
            content=validated_data['content'],
            application=validated_data['app_token']
        )
        notification.clients.set(validated_data['users'])
        handle_notification(notification, True)
