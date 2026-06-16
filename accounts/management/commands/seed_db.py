from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
import uuid


class Command(BaseCommand):
    help = 'Charge les données de démonstration COFINANCE CI'

    def handle(self, *args, **kwargs):
        self.stdout.write('Chargement des données de démonstration...')
        self.create_users()
        self.create_produits()
        self.create_credits()
        self.create_souscriptions()
        self.create_conversations()
        self.create_notifications()
        self.stdout.write(self.style.SUCCESS('Données chargées avec succès.'))

    def create_users(self):
        from accounts.models import User
        users = [
            dict(username='admin', email='admin@cofinance.ci', first_name='Administrateur',
                 last_name='COFINANCE', role='admin', telephone='+225 01 01 01 01', region='Abidjan'),
            dict(username='agent_kone', email='kone@cofinance.ci', first_name='Mamadou',
                 last_name='Kone', role='agent', telephone='+225 07 01 02 03', region='Abidjan'),
            dict(username='cliente_adjoua', email='adjoua@gmail.com', first_name='Adjoua',
                 last_name='Bamba', role='client', telephone='+225 05 10 20 30', region='Bouake'),
            dict(username='client_kouassi', email='kouassi@gmail.com', first_name='Kouassi',
                 last_name='Aka', role='client', telephone='+225 01 02 03 04', region='Daloa'),
            dict(username='cliente_fatou', email='fatou@gmail.com', first_name='Fatou',
                 last_name='Diallo', role='client', telephone='+225 07 08 09 10', region='San Pedro'),
        ]
        for u in users:
            user, created = User.objects.get_or_create(username=u['username'], defaults=u)
            if created:
                user.set_password('CofinanceCI2026!')
            # Rendre l'admin superuser et forcer le rôle admin
            if u['username'] == 'admin':
                user.role = 'admin'
                user.is_superuser = True
                user.is_staff = True
                user.set_password('CofinanceCI2026!')
                user.save()
                self.stdout.write(f'  Admin mis à jour : {u["username"]} (role: {user.role})')
            elif created:
                self.stdout.write(f'  Utilisateur créé : {u["username"]} (role: {u["role"]})')

    def create_produits(self):
        from assurances.models import ProduitAssurance
        produits = [
            dict(nom='Assurance Vie Essentielle', type_assurance='vie',
                 description='Couverture vie de base pour micro-entrepreneurs.',
                 prime_mensuelle=2500, capital_garanti=1000000, duree_mois=12),
            dict(nom='Assurance Deces-Invalidite Plus', type_assurance='deces_invalidite',
                 description='Protection complete deces et invalidite permanente.',
                 prime_mensuelle=4000, capital_garanti=2500000, duree_mois=24),
        ]
        for p in produits:
            if not ProduitAssurance.objects.filter(nom=p['nom']).exists():
                ProduitAssurance.objects.create(**p)
                self.stdout.write(f'  Produit cree : {p["nom"]}')

    def create_credits(self):
        from accounts.models import User
        from credits.models import DemandeCredit, Echeance
        from decimal import Decimal

        try:
            adjoua = User.objects.get(username='cliente_adjoua')
            kouassi = User.objects.get(username='client_kouassi')
            agent = User.objects.get(username='agent_kone')
        except User.DoesNotExist:
            return

        credits_data = [
            dict(client=adjoua, agent=agent, montant_demande=250000, duree_mois=6,
                 periodicite='mensuel', objet_credit='Achat de stock pour boutique de tissu',
                 statut='approuvee', score_eligibilite=75,
                 commentaire_agent='Dossier complet, historique satisfaisant.'),
            dict(client=kouassi, montant_demande=100000, duree_mois=3,
                 periodicite='mensuel', objet_credit='Fonds de roulement vente de legumes',
                 statut='soumise', score_eligibilite=65),
            dict(client=adjoua, agent=agent, montant_demande=500000, duree_mois=12,
                 periodicite='mensuel', objet_credit='Extension de commerce de pagne',
                 statut='decaissee', score_eligibilite=80),
        ]

        for c in credits_data:
            credit = DemandeCredit.objects.create(**c)
            montant = Decimal(str(credit.montant_demande))
            taux = Decimal(str(credit.taux_interet)) / Decimal('100')
            principal = montant / credit.duree_mois
            for i in range(1, credit.duree_mois + 1):
                mois = date.today().month + i
                annee = date.today().year + (mois - 1) // 12
                mois = ((mois - 1) % 12) + 1
                date_echeance = date.today().replace(year=annee, month=mois)
                solde = montant - (principal * (i - 1))
                interet = solde * taux
                Echeance.objects.create(
                    credit=credit, numero=i, date_echeance=date_echeance,
                    montant_principal=round(principal, 2),
                    montant_interet=round(interet, 2),
                    montant_total=round(principal + interet, 2),
                )
            self.stdout.write(f'  Credit cree : {credit}')

    def create_souscriptions(self):
        from accounts.models import User
        from assurances.models import ProduitAssurance, Souscription

        try:
            adjoua = User.objects.get(username='cliente_adjoua')
            produit = ProduitAssurance.objects.first()
        except (User.DoesNotExist, ProduitAssurance.DoesNotExist):
            return

        if not Souscription.objects.filter(client=adjoua).exists():
            Souscription.objects.create(
                client=adjoua, produit=produit,
                date_debut=date.today(),
                date_fin=date.today().replace(year=date.today().year + 1),
                statut='active',
                numero_police=f'COF-{uuid.uuid4().hex[:8].upper()}',
            )
            self.stdout.write('  Souscription creee.')

    def create_conversations(self):
        from accounts.models import User
        from support.models import Conversation, Message

        try:
            adjoua = User.objects.get(username='cliente_adjoua')
            kouassi = User.objects.get(username='client_kouassi')
            agent = User.objects.get(username='agent_kone')
        except User.DoesNotExist:
            return

        # Première conversation avec cliente_adjoua
        if not Conversation.objects.filter(client=adjoua).exists():
            conv = Conversation.objects.create(
                client=adjoua, agent=agent,
                sujet='Question sur mon echeancier de remboursement',
                statut='en_cours',
            )
            Message.objects.create(
                conversation=conv, expediteur=adjoua,
                contenu='Bonjour, je voudrais savoir quand tombe ma prochaine echeance.',
            )
            Message.objects.create(
                conversation=conv, expediteur=agent,
                contenu='Bonjour Adjoua, votre prochaine echeance est le 15 juin 2026 pour 44 792 FCFA.',
            )
            self.stdout.write('  Conversation 1 et messages crees.')

        # Deuxième conversation avec client_kouassi
        if not Conversation.objects.filter(client=kouassi).exists():
            conv2 = Conversation.objects.create(
                client=kouassi, agent=agent,
                sujet='Demande de renseignements sur les taux d\'interet',
                statut='ouverte',
            )
            Message.objects.create(
                conversation=conv2, expediteur=kouassi,
                contenu='Bonjour, quels sont les taux d\'interet actuels pour les credits de 100 000 FCFA ?',
            )
            Message.objects.create(
                conversation=conv2, expediteur=agent,
                contenu='Bonjour Kouassi, nos taux actuels sont de 12% annuel pour les credits de ce montant.',
            )
            self.stdout.write('  Conversation 2 et messages crees.')

    def create_notifications(self):
        from accounts.models import User
        from notifications.models import Notification

        try:
            adjoua = User.objects.get(username='cliente_adjoua')
        except User.DoesNotExist:
            return

        notifs = [
            dict(titre='Demande de credit approuvee',
                 message='Votre demande de credit de 250 000 FCFA a ete approuvee.',
                 type_notif='credit'),
            dict(titre='Rappel de remboursement',
                 message='Votre echeance de 44 792 FCFA arrive dans 3 jours.',
                 type_notif='remboursement'),
            dict(titre='Souscription confirmee',
                 message='Votre souscription Assurance Vie Essentielle est active.',
                 type_notif='assurance'),
        ]
        for n in notifs:
            Notification.objects.create(destinataire=adjoua, **n)
        self.stdout.write('  Notifications creees.')