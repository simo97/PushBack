from django.urls import path
from .views import (
    ApplicationListView,
    ApplicationCreateView,
    ApplicationDetailView,
    ApplicationDeleteView
)

app_name = 'webapp'


urlpatterns = [
    path('', ApplicationListView.as_view(), name='application-list'),
    path('<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('application-new/', ApplicationCreateView.as_view(), name='application-new'),
    path('<int:pk>/application-delete/', ApplicationDeleteView.as_view(), name='application-delete'),
]
