from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User


class Conversation(models.Model):
    STATUT_OUVERTE = 'ouverte'
    STATUT_EN_COURS = 'en_cours'
    STATUT_FERMEE = 'fermee'

    STATUT_CHOICES = [
        (STATUT_OUVERTE, 'Ouverte'),
        (STATUT_EN_COURS, 'En cours'),
        (STATUT_FERMEE, 'Fermee'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_client')
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='conversations_agent')
    sujet = models.CharField(max_length=255)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default=STATUT_OUVERTE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation #{self.id} - {self.client.username} ({self.statut})"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_envoyes')
    contenu = models.TextField()
    lu = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message de {self.expediteur.username} dans conversation #{self.conversation.id}"