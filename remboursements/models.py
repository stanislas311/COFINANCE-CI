from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User
from credits.models import Echeance


class Paiement(models.Model):
    MOYEN_ORANGE = 'orange_money'
    MOYEN_WAVE = 'wave'
    MOYEN_MTN = 'mtn_momo'
    MOYEN_ESPECES = 'especes'

    MOYEN_CHOICES = [
        (MOYEN_ORANGE, 'Orange Money'),
        (MOYEN_WAVE, 'Wave'),
        (MOYEN_MTN, 'MTN MoMo'),
        (MOYEN_ESPECES, 'Especes'),
    ]

    echeance = models.OneToOneField(Echeance, on_delete=models.CASCADE, related_name='paiement')
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='paiements_enregistres')
    montant_paye = models.DecimalField(max_digits=12, decimal_places=2)
    moyen_paiement = models.CharField(max_length=15, choices=MOYEN_CHOICES)
    reference_transaction = models.CharField(max_length=100, blank=True)
    date_paiement = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement echeance #{self.echeance.id} - {self.montant_paye} FCFA"