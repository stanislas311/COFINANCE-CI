from django.db import models
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

# Create your models here.
from django.db import models
from accounts.models import User


class DemandeCredit(models.Model):
    STATUT_SOUMISE = 'soumise'
    STATUT_EN_ANALYSE = 'en_analyse'
    STATUT_APPROUVEE = 'approuvee'
    STATUT_DECAISSEE = 'decaissee'
    STATUT_REJETEE = 'rejetee'

    STATUT_CHOICES = [
        (STATUT_SOUMISE, 'Soumise'),
        (STATUT_EN_ANALYSE, 'En analyse'),
        (STATUT_APPROUVEE, 'Approuvee'),
        (STATUT_DECAISSEE, 'Decaissee'),
        (STATUT_REJETEE, 'Rejetee'),
    ]

    PERIODICITE_HEBDO = 'hebdomadaire'
    PERIODICITE_MENSUEL = 'mensuel'

    PERIODICITE_CHOICES = [
        (PERIODICITE_HEBDO, 'Hebdomadaire'),
        (PERIODICITE_MENSUEL, 'Mensuel'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demandes_credit')
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='dossiers_traites')
    montant_demande = models.DecimalField(max_digits=12, decimal_places=2)
    duree_mois = models.PositiveIntegerField()
    periodicite = models.CharField(max_length=15, choices=PERIODICITE_CHOICES, default=PERIODICITE_MENSUEL)
    taux_interet = models.DecimalField(max_digits=5, decimal_places=2, default=2.5)
    objet_credit = models.TextField()
    piece_justificative = models.FileField(upload_to='credits/pieces/', null=True, blank=True)
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default=STATUT_SOUMISE)
    score_eligibilite = models.IntegerField(null=True, blank=True)
    commentaire_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Credit #{self.id} - {self.client.username} - {self.montant_demande} FCFA"

    def calculer_score(self):
        score = 50
        if self.montant_demande <= 100000:
            score += 20
        elif self.montant_demande <= 500000:
            score += 10
        if self.duree_mois <= 6:
            score += 15
        elif self.duree_mois <= 12:
            score += 10
        credits_passes = DemandeCredit.objects.filter(
            client=self.client,
            statut=self.STATUT_DECAISSEE
        ).count()
        score += min(credits_passes * 5, 15)
        return min(score, 100)


class Echeance(models.Model):
    STATUT_EN_ATTENTE = 'en_attente'
    STATUT_PAYEE = 'payee'
    STATUT_EN_RETARD = 'en_retard'

    STATUT_CHOICES = [
        (STATUT_EN_ATTENTE, 'En attente'),
        (STATUT_PAYEE, 'Payee'),
        (STATUT_EN_RETARD, 'En retard'),
    ]

    credit = models.ForeignKey(DemandeCredit, on_delete=models.CASCADE, related_name='echeances')
    numero = models.PositiveIntegerField()
    date_echeance = models.DateField()
    montant_principal = models.DecimalField(max_digits=12, decimal_places=2)
    montant_interet = models.DecimalField(max_digits=12, decimal_places=2)
    montant_total = models.DecimalField(max_digits=12, decimal_places=2)
    montant_penalite = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    statut = models.CharField(max_length=12, choices=STATUT_CHOICES, default=STATUT_EN_ATTENTE)
    date_paiement = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['numero']

    def __str__(self):
        return f"Echeance #{self.numero} - Credit #{self.credit.id}"

    def calculer_penalite(self):
        """
        Calcule automatiquement les pénalités de retard.
        Taux de pénalité : 2% du montant total par jour de retard.
        """
        if self.statut != 'en_retard' or self.date_echeance >= timezone.now().date():
            return Decimal('0.00')
        
        jours_retard = (timezone.now().date() - self.date_echeance).days
        if jours_retard <= 0:
            return Decimal('0.00')
        
        taux_penalite = Decimal('0.02')  # 2% par jour de retard
        penalite = self.montant_total * taux_penalite * Decimal(jours_retard)
        return round(penalite, 2)

    def mettre_a_jour_statut_et_penalite(self):
        """
        Met à jour le statut de l'échéance et calcule les pénalités si en retard.
        """
        if self.statut == 'payee':
            return
        
        aujourd_hui = timezone.now().date()
        if aujourd_hui > self.date_echeance:
            self.statut = 'en_retard'
            self.montant_penalite = self.calculer_penalite()
            self.save()