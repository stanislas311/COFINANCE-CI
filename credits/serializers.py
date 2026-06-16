from rest_framework import serializers
from .models import DemandeCredit, Echeance
from datetime import date, timedelta
from decimal import Decimal


class EcheanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Echeance
        fields = '__all__'
        read_only_fields = ['id']


class DemandeCreditSerializer(serializers.ModelSerializer):
    echeances = EcheanceSerializer(many=True, read_only=True)
    client_nom = serializers.SerializerMethodField()
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)

    class Meta:
        model = DemandeCredit
        fields = '__all__'
        read_only_fields = ['id', 'client', 'score_eligibilite', 'created_at', 'updated_at']

    def get_client_nom(self, obj):
        return obj.client.get_full_name() or obj.client.username


class DemandeCreditCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeCredit
        fields = [
            'montant_demande', 'duree_mois', 'periodicite',
            'objet_credit', 'piece_justificative',
        ]

    def create(self, validated_data):
        credit = DemandeCredit(**validated_data)
        credit.score_eligibilite = credit.calculer_score()
        credit.save()
        self.generer_echeancier(credit)
        return credit

    def generer_echeancier(self, credit):
        montant = Decimal(str(credit.montant_demande))
        taux = Decimal(str(credit.taux_interet)) / Decimal('100')
        duree = credit.duree_mois
        principal_par_echeance = montant / duree
        date_debut = date.today()

        for i in range(1, duree + 1):
            if credit.periodicite == 'hebdomadaire':
                date_echeance = date_debut + timedelta(weeks=i)
            else:
                mois = date_debut.month + i
                annee = date_debut.year + (mois - 1) // 12
                mois = ((mois - 1) % 12) + 1
                date_echeance = date_debut.replace(year=annee, month=mois)

            solde_restant = montant - (principal_par_echeance * (i - 1))
            interet = solde_restant * taux
            total = principal_par_echeance + interet

            Echeance.objects.create(
                credit=credit,
                numero=i,
                date_echeance=date_echeance,
                montant_principal=round(principal_par_echeance, 2),
                montant_interet=round(interet, 2),
                montant_total=round(total, 2),
            )