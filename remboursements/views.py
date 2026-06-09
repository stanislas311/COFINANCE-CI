from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Paiement
from .serializers import PaiementSerializer
from credits.models import Echeance, DemandeCredit
from django.utils import timezone


class PaiementListView(generics.ListAPIView):
    serializer_class = PaiementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'agent']:
            return Paiement.objects.all()
        return Paiement.objects.filter(echeance__credit__client=user)


class EnregistrerPaiementView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, echeance_id):
        if request.user.role not in ['admin', 'agent']:
            return Response({'detail': 'Permission refusee.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            echeance = Echeance.objects.get(pk=echeance_id)
        except Echeance.DoesNotExist:
            return Response({'detail': 'Echeance introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        if hasattr(echeance, 'paiement'):
            return Response({'detail': 'Cette echeance est deja payee.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PaiementSerializer(data=request.data)
        if serializer.is_valid():
            paiement = serializer.save(agent=request.user, echeance=echeance)
            echeance.statut = 'payee'
            echeance.date_paiement = paiement.date_paiement
            echeance.save()

            from notifications.utils import creer_notification
            creer_notification(
                destinataire=echeance.credit.client,
                titre='Paiement enregistre',
                message=f'Votre paiement de {paiement.montant_paye} FCFA pour l echeance #{echeance.numero} a ete enregistre.',
                type_notif='remboursement'
            )
            return Response(PaiementSerializer(paiement).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)