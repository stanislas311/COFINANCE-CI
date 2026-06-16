from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Envoie les alertes automatiques : J-3, J+1, pénalités de retard, expiration assurance J-15'

    def handle(self, *args, **kwargs):
        self.stdout.write('Exécution des alertes automatiques...')
        
        # 1. Mettre à jour les échéances en retard et calculer les pénalités
        self.mettre_a_jour_echeances_en_retard()
        
        # 2. Envoyer les alertes J-3 avant échéance
        self.envoyer_alertes_echeances_j_moins_3()
        
        # 3. Envoyer les alertes J+1 après échéance
        self.envoyer_alertes_echeances_j_plus_1()
        
        # 4. Envoyer les alertes d'expiration assurance 15 jours avant
        self.envoyer_alertes_expiration_assurance()
        
        # 5. Mettre à jour les souscriptions expirées
        self.mettre_a_jour_souscriptions_expirees()
        
        self.stdout.write(self.style.SUCCESS('Toutes les alertes ont été envoyées avec succès.'))

    def mettre_a_jour_echeances_en_retard(self):
        """Met à jour le statut des échéances en retard et calcule les pénalités."""
        from credits.models import Echeance
        
        echeances = Echeance.objects.filter(statut='en_attente')
        count = 0
        for echeance in echeances:
            echeance.mettre_a_jour_statut_et_penalite()
            count += 1
        
        self.stdout.write(f'  ✓ {count} échéances mises à jour (statut et pénalités)')

    def envoyer_alertes_echeances_j_moins_3(self):
        """Envoie des alertes 3 jours avant l'échéance."""
        from credits.models import Echeance
        from notifications.utils import creer_notification
        
        aujourdhui = timezone.now().date()
        date_cible = aujourdhui + timedelta(days=3)
        
        echeances = Echeance.objects.filter(
            statut='en_attente',
            date_echeance=date_cible
        )
        
        count = 0
        for echeance in echeances:
            creer_notification(
                destinataire=echeance.credit.client,
                titre='Rappel d\'échéance',
                message=f'Votre échéance #{echeance.numero} de {echeance.montant_total} FCFA arrive dans 3 jours, le {echeance.date_echeance}.',
                type_notif='remboursement'
            )
            count += 1
        
        self.stdout.write(f'  ✓ {count} alertes J-3 envoyées')

    def envoyer_alertes_echeances_j_plus_1(self):
        """Envoie des alertes 1 jour après l'échéance non payée."""
        from credits.models import Echeance
        from notifications.utils import creer_notification
        
        aujourdhui = timezone.now().date()
        date_cible = aujourdhui - timedelta(days=1)
        
        echeances = Echeance.objects.filter(
            statut='en_attente',
            date_echeance=date_cible
        )
        
        count = 0
        for echeance in echeances:
            # Mettre à jour le statut en retard
            echeance.mettre_a_jour_statut_et_penalite()
            
            creer_notification(
                destinataire=echeance.credit.client,
                titre='Échéance en retard',
                message=f'Votre échéance #{echeance.numero} de {echeance.montant_total} FCFA est en retard depuis le {echeance.date_echeance}. Pénalités appliquées : {echeance.montant_penalite} FCFA.',
                type_notif='remboursement'
            )
            count += 1
        
        self.stdout.write(f'  ✓ {count} alertes J+1 envoyées')

    def envoyer_alertes_expiration_assurance(self):
        """Envoie des alertes 15 jours avant l'expiration des assurances."""
        from assurances.models import Souscription
        from notifications.utils import creer_notification
        
        aujourdhui = timezone.now().date()
        date_cible = aujourdhui + timedelta(days=15)
        
        souscriptions = Souscription.objects.filter(
            statut='active',
            date_fin=date_cible
        )
        
        count = 0
        for souscription in souscriptions:
            creer_notification(
                destinataire=souscription.client,
                titre='Assurance bientôt expirée',
                message=f'Votre assurance {souscription.produit.nom} (police {souscription.numero_police}) expire dans 15 jours, le {souscription.date_fin}. Renouvelez-la pour continuer à bénéficier de la couverture.',
                type_notif='assurance'
            )
            count += 1
        
        self.stdout.write(f'  ✓ {count} alertes d\'expiration envoyées')

    def mettre_a_jour_souscriptions_expirees(self):
        """Met à jour le statut des souscriptions expirées."""
        from assurances.models import Souscription
        from notifications.utils import creer_notification
        
        aujourdhui = timezone.now().date()
        
        souscriptions = Souscription.objects.filter(
            statut='active',
            date_fin__lt=aujourdhui
        )
        
        count = 0
        for souscription in souscriptions:
            souscription.statut = 'expiree'
            souscription.save()
            
            creer_notification(
                destinataire=souscription.client,
                titre='Assurance expirée',
                message=f'Votre assurance {souscription.produit.nom} (police {souscription.numero_police}) a expiré le {souscription.date_fin}. Contactez-nous pour la renouveler.',
                type_notif='assurance'
            )
            count += 1
        
        self.stdout.write(f'  ✓ {count} souscriptions mises à jour comme expirées')
