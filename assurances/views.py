from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import ProduitAssurance, Souscription
from .serializers import ProduitAssuranceSerializer, SouscriptionSerializer, SouscriptionCreateSerializer


class ProduitAssuranceListView(generics.ListAPIView):
    serializer_class = ProduitAssuranceSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProduitAssurance.objects.filter(actif=True)


class SouscriptionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SouscriptionCreateSerializer
        return SouscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'agent']:
            return Souscription.objects.all()
        return Souscription.objects.filter(client=user)

    def get_serializer_context(self):
        return {'request': self.request}


class SouscriptionDetailView(generics.RetrieveAPIView):
    serializer_class = SouscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'agent']:
            return Souscription.objects.all()
        return Souscription.objects.filter(client=user)