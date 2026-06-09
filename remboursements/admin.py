from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Paiement

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ['id', 'echeance', 'montant_paye', 'moyen_paiement', 'date_paiement', 'agent']
    list_filter = ['moyen_paiement']