from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DemandeCredit, Echeance
from .serializers import DemandeCreditSerializer, DemandeCreditCreateSerializer, EcheanceSerializer


class DemandeCreditListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DemandeCreditCreateSerializer
        return DemandeCreditSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'agent']:
            return DemandeCredit.objects.all()
        return DemandeCredit.objects.filter(client=user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class DemandeCreditDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return DemandeCreditSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'agent']:
            return DemandeCredit.objects.all()
        return DemandeCredit.objects.filter(client=user)


class ChangerStatutCreditView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        if request.user.role not in ['admin', 'agent']:
            return Response({'detail': 'Permission refusee.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            credit = DemandeCredit.objects.get(pk=pk)
        except DemandeCredit.DoesNotExist:
            return Response({'detail': 'Credit introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        nouveau_statut = request.data.get('statut')
        statuts_valides = ['en_analyse', 'approuvee', 'decaissee', 'rejetee']
        if nouveau_statut not in statuts_valides:
            return Response({'detail': 'Statut invalide.'}, status=status.HTTP_400_BAD_REQUEST)

        credit.statut = nouveau_statut
        credit.agent = request.user
        if request.data.get('commentaire'):
            credit.commentaire_agent = request.data['commentaire']
        credit.save()

        from notifications.utils import creer_notification
        creer_notification(
            destinataire=credit.client,
            titre='Mise a jour de votre demande de credit',
            message=f'Votre demande de credit #{credit.id} est maintenant : {credit.get_statut_display()}',
            type_notif='credit'
        )

        return Response(DemandeCreditSerializer(credit).data)


class EcheanceListView(generics.ListAPIView):
    serializer_class = EcheanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Echeance.objects.filter(credit_id=self.kwargs['credit_id'])