from rest_framework import serializers
from .models import Paiement
from credits.serializers import EcheanceSerializer


class PaiementSerializer(serializers.ModelSerializer):
    echeance_detail = EcheanceSerializer(source='echeance', read_only=True)
    agent_nom = serializers.SerializerMethodField()

    class Meta:
        model = Paiement
        fields = '__all__'
        read_only_fields = ['id', 'agent', 'created_at']

    def get_agent_nom(self, obj):
        if obj.agent:
            return obj.agent.get_full_name() or obj.agent.username
        return None