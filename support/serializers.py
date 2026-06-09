from rest_framework import serializers
from .models import Conversation, Message
from accounts.serializers import UserProfileSerializer


class MessageSerializer(serializers.ModelSerializer):
    expediteur_nom = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'expediteur', 'expediteur_nom', 'contenu', 'lu', 'timestamp']
        read_only_fields = ['id', 'expediteur', 'timestamp']

    def get_expediteur_nom(self, obj):
        return obj.expediteur.get_full_name() or obj.expediteur.username


class ConversationSerializer(serializers.ModelSerializer):
    client_nom = serializers.SerializerMethodField()
    agent_nom = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)
    dernier_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'client', 'client_nom', 'agent', 'agent_nom',
            'sujet', 'statut', 'messages', 'dernier_message',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'client', 'created_at', 'updated_at']

    def get_client_nom(self, obj):
        return obj.client.get_full_name() or obj.client.username

    def get_agent_nom(self, obj):
        if obj.agent:
            return obj.agent.get_full_name() or obj.agent.username
        return None

    def get_dernier_message(self, obj):
        dernier = obj.messages.last()
        if dernier:
            return {
                'contenu': dernier.contenu,
                'timestamp': dernier.timestamp.isoformat(),
                'expediteur': dernier.expediteur.username,
            }
        return None


class ConversationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'sujet']
        read_only_fields = ['id']