from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ProduitAssurance, Souscription

@admin.register(ProduitAssurance)
class ProduitAssuranceAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type_assurance', 'prime_mensuelle', 'capital_garanti', 'actif']
    list_filter = ['type_assurance', 'actif']

@admin.register(Souscription)
class SouscriptionAdmin(admin.ModelAdmin):
    list_display = ['numero_police', 'client', 'produit', 'date_debut', 'date_fin', 'statut']
    list_filter = ['statut']