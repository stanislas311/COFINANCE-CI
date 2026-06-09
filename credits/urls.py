from django.urls import path
from .views import (
    DemandeCreditListCreateView,
    DemandeCreditDetailView,
    ChangerStatutCreditView,
    EcheanceListView,
)

urlpatterns = [
    path('', DemandeCreditListCreateView.as_view(), name='credit-list'),
    path('<int:pk>/', DemandeCreditDetailView.as_view(), name='credit-detail'),
    path('<int:pk>/statut/', ChangerStatutCreditView.as_view(), name='credit-statut'),
    path('<int:credit_id>/echeances/', EcheanceListView.as_view(), name='echeance-list'),
]