from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Conversation, Message
from .serializers import ConversationSerializer, ConversationCreateSerializer, MessageSerializer


class ConversationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'agent']:
            return Conversation.objects.all()
        return Conversation.objects.filter(client=user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class ConversationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'agent']:
            return Conversation.objects.all()
        return Conversation.objects.filter(client=user)


class AssignerAgentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        if request.user.role not in ['admin', 'agent']:
            return Response({'detail': 'Permission refusee.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            conversation = Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            return Response({'detail': 'Conversation introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        conversation.agent = request.user
        conversation.statut = Conversation.STATUT_EN_COURS
        conversation.save()
        return Response(ConversationSerializer(conversation).data)


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(conversation_id=self.kwargs['conversation_id'])

    def perform_create(self, serializer):
        serializer.save(
            expediteur=self.request.user,
            conversation_id=self.kwargs['conversation_id']
        )