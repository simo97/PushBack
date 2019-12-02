from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import RegistrationSerializer, NotifySerializer


class BaseView(CreateAPIView):
    success_response_data = None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response(self.success_response_data, status=status.HTTP_200_OK)


class RegistrationView(BaseView):
    serializer_class = RegistrationSerializer
    success_response_data = {'code': 'success', 'details': 'Users registered with success'}


class NotifyView(BaseView):
    serializer_class = NotifySerializer
    success_response_data = {'code': 'success', 'details': 'Notifications sent with success'}
