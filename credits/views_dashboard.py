from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta

from credits.models import DemandeCredit, Echeance
from remboursements.models import Paiement
from assurances.models import Souscription
from support.models import Conversation
from accounts.models import User


class DashboardAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role not in ['admin', 'agent']:
            from rest_framework import status
            return Response({'detail': 'Permission refusee.'}, status=status.HTTP_403_FORBIDDEN)

        # Filtres optionnels
        date_debut = request.query_params.get('date_debut')
        date_fin = request.query_params.get('date_fin')
        agent_id = request.query_params.get('agent_id')
        region = request.query_params.get('region')

        credits_qs = DemandeCredit.objects.all()
        if date_debut:
            credits_qs = credits_qs.filter(created_at__date__gte=date_debut)
        if date_fin:
            credits_qs = credits_qs.filter(created_at__date__lte=date_fin)
        if agent_id:
            credits_qs = credits_qs.filter(agent_id=agent_id)
        if region:
            credits_qs = credits_qs.filter(client__region__icontains=region)

        # Credits par statut
        credits_par_statut = dict(
            credits_qs.values('statut').annotate(total=Count('id')).values_list('statut', 'total')
        )

        # Montant total décaissé
        montant_decaisse = credits_qs.filter(statut='decaissee').aggregate(
            total=Sum('montant_demande')
        )['total'] or 0

        # Taux de recouvrement
        echeances_qs = Echeance.objects.filter(credit__in=credits_qs)
        total_echeances = echeances_qs.count()
        echeances_payees = echeances_qs.filter(statut='payee').count()
        taux_recouvrement = round(
            (echeances_payees / total_echeances * 100) if total_echeances > 0 else 0, 2
        )

        # Souscriptions actives
        souscriptions_actives = Souscription.objects.filter(statut='active').count()

        # Conversations support ouvertes
        conversations_ouvertes = Conversation.objects.filter(
            statut__in=['ouverte', 'en_cours']
        ).count()

        # Nouveaux clients ce mois
        debut_mois = timezone.now().replace(day=1, hour=0, minute=0, second=0)
        nouveaux_clients = User.objects.filter(
            role='client', created_at__gte=debut_mois
        ).count()

        # Echéances en retard
        echeances_retard = Echeance.objects.filter(
            statut='en_attente',
            date_echeance__lt=timezone.now().date()
        ).count()

        return Response({
            'credits': {
                'par_statut': credits_par_statut,
                'montant_total_decaisse': montant_decaisse,
                'taux_recouvrement': taux_recouvrement,
                'echeances_en_retard': echeances_retard,
            },
            'assurances': {
                'souscriptions_actives': souscriptions_actives,
            },
            'support': {
                'conversations_ouvertes': conversations_ouvertes,
            },
            'clients': {
                'nouveaux_ce_mois': nouveaux_clients,
                'total': User.objects.filter(role='client').count(),
            },
        })