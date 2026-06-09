from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User


class ProduitAssurance(models.Model):
    TYPE_VIE = 'vie'
    TYPE_DECES = 'deces_invalidite'

    TYPE_CHOICES = [
        (TYPE_VIE, 'Assurance Vie'),
        (TYPE_DECES, 'Deces-Invalidite'),
    ]

    nom = models.CharField(max_length=100)
    type_assurance = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    prime_mensuelle = models.DecimalField(max_digits=10, decimal_places=2)
    capital_garanti = models.DecimalField(max_digits=12, decimal_places=2)
    duree_mois = models.PositiveIntegerField()
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} - {self.prime_mensuelle} FCFA/mois"


class Souscription(models.Model):
    STATUT_ACTIVE = 'active'
    STATUT_EXPIREE = 'expiree'
    STATUT_RESILIEE = 'resiliee'

    STATUT_CHOICES = [
        (STATUT_ACTIVE, 'Active'),
        (STATUT_EXPIREE, 'Expiree'),
        (STATUT_RESILIEE, 'Resiliee'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='souscriptions')
    produit = models.ForeignKey(ProduitAssurance, on_delete=models.CASCADE, related_name='souscriptions')
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default=STATUT_ACTIVE)
    numero_police = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Police {self.numero_police} - {self.client.username}"