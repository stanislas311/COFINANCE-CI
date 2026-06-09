from django.urls import path
from .views import NotificationListView, MarquerLuView, MarquerToutLuView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/lire/', MarquerLuView.as_view(), name='notification-lire'),
    path('tout-lire/', MarquerToutLuView.as_view(), name='notification-tout-lire'),
]