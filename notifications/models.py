from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User


class Notification(models.Model):
    TYPE_CREDIT = 'credit'
    TYPE_REMBOURSEMENT = 'remboursement'
    TYPE_ASSURANCE = 'assurance'
    TYPE_SUPPORT = 'support'
    TYPE_GENERAL = 'general'

    TYPE_CHOICES = [
        (TYPE_CREDIT, 'Credit'),
        (TYPE_REMBOURSEMENT, 'Remboursement'),
        (TYPE_ASSURANCE, 'Assurance'),
        (TYPE_SUPPORT, 'Support'),
        (TYPE_GENERAL, 'General'),
    ]

    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    titre = models.CharField(max_length=200)
    message = models.TextField()
    type_notif = models.CharField(max_length=15, choices=TYPE_CHOICES, default=TYPE_GENERAL)
    lu = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notif pour {self.destinataire.username} - {self.titre}"