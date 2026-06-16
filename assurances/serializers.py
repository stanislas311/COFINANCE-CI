from rest_framework import serializers
from .models import ProduitAssurance, Souscription


class ProduitAssuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduitAssurance
        fields = '__all__'


class SouscriptionSerializer(serializers.ModelSerializer):
    produit_detail = ProduitAssuranceSerializer(source='produit', read_only=True)
    client_nom = serializers.SerializerMethodField()
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)

    class Meta:
        model = Souscription
        fields = '__all__'
        read_only_fields = ['id', 'client', 'numero_police', 'statut', 'created_at']

    def get_client_nom(self, obj):
        return obj.client.get_full_name() or obj.client.username


class SouscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Souscription
        fields = ['produit', 'date_debut']

    def create(self, validated_data):
        import uuid
        from datetime import timedelta
        produit = validated_data['produit']
        date_debut = validated_data['date_debut']
        import calendar
        month = ((date_debut.month + produit.duree_mois - 1) % 12) + 1
        year = date_debut.year + (date_debut.month + produit.duree_mois - 1) // 12
        day = min(date_debut.day, calendar.monthrange(year, month)[1])
        date_fin = date_debut.replace(year=year, month=month, day=day)
        numero_police = f"COF-{uuid.uuid4().hex[:8].upper()}"
        return Souscription.objects.create(
            client=self.context['request'].user,
            produit=produit,
            date_debut=date_debut,
            date_fin=date_fin,
            numero_police=numero_police,
        )