from django.urls import path
from .views import PaiementListView, EnregistrerPaiementView

urlpatterns = [
    path('', PaiementListView.as_view(), name='paiement-list'),
    path('echeance/<int:echeance_id>/payer/', EnregistrerPaiementView.as_view(), name='enregistrer-paiement'),
]