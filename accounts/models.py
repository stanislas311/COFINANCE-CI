from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CLIENT = 'client'
    ROLE_AGENT = 'agent'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
        (ROLE_CLIENT, 'Client'),
        (ROLE_AGENT, 'Agent de terrain'),
        (ROLE_ADMIN, 'Administrateur'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_CLIENT)
    telephone = models.CharField(max_length=20, blank=True)
    region = models.CharField(max_length=100, blank=True)
    adresse = models.TextField(blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    piece_identite = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to='profils/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    @property
    def is_client(self):
        return self.role == self.ROLE_CLIENT

    @property
    def is_agent(self):
        return self.role == self.ROLE_AGENT

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN