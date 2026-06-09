from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/support/(?P<conversation_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]