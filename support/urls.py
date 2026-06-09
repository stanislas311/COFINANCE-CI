from django.urls import path
from .views import (
    ConversationListCreateView,
    ConversationDetailView,
    AssignerAgentView,
    MessageListCreateView,
)

urlpatterns = [
    path('conversations/', ConversationListCreateView.as_view(), name='conversation-list'),
    path('conversations/<int:pk>/', ConversationDetailView.as_view(), name='conversation-detail'),
    path('conversations/<int:pk>/assigner/', AssignerAgentView.as_view(), name='conversation-assigner'),
    path('conversations/<int:conversation_id>/messages/', MessageListCreateView.as_view(), name='message-list'),
]