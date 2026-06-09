from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import DemandeCredit, Echeance

@admin.register(DemandeCredit)
class DemandeCreditAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'montant_demande', 'statut', 'score_eligibilite', 'created_at']
    list_filter = ['statut', 'periodicite']

@admin.register(Echeance)
class EcheanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'credit', 'numero', 'date_echeance', 'montant_total', 'statut']
    list_filter = ['statut']