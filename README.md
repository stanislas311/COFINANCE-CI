# COFINANCE CI — Plateforme Digitale de Microfinance

Plateforme de gestion de microcrédits, assurance mobile et support client en temps réel.
Développée avec Django REST Framework + Django Channels (WebSocket).

---

## Stack technique

- Python 3.11+
- Django 5.x
- Django REST Framework
- djangorestframework-simplejwt (JWT)
- Django Channels (WebSocket)
- drf-spectacular (Swagger/Redoc)
- SQLite (dev) / PostgreSQL (prod)

---

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/stanislas311/COFINANCE-CI
cd COFINANCE-CI
```

### 2. Créer et activer l'environnement virtuel

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Appliquer les migrations

```bash
python manage.py migrate
```

### 5. Charger les données de démonstration

```bash
python manage.py seed_db
```

### 6. Créer un superutilisateur (optionnel)

```bash
python manage.py createsuperuser
```

*Note : La commande `seed_db` crée déjà un utilisateur admin avec le rôle administrateur.*

### 7. Lancer le serveur

```bash
python -m daphne -p 8000 config.asgi:application
```

---

## Alertes automatiques

Le système inclut une commande management pour envoyer les alertes automatiques :

- **Alertes J-3** : Rappel 3 jours avant chaque échéance
- **Alertes J+1** : Notification 1 jour après échéance non payée (avec pénalités)
- **Pénalités de retard** : Calcul automatique (2% par jour de retard)
- **Alertes assurance J-15** : Notification 15 jours avant expiration des assurances

Pour exécuter les alertes manuellement ou via planificateur système (cron/Task Scheduler) :

```bash
python manage.py send_alerts
```

**En production** : Configurez cette commande pour s'exécuter quotidiennement (par exemple via cron sur Linux ou Task Scheduler sur Windows).

---

## Accès

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/api/docs/ | Documentation Swagger |
| http://127.0.0.1:8000/api/redoc/ | Documentation Redoc |
| http://127.0.0.1:8000/admin/ | Interface d'administration |
| http://127.0.0.1:8000/chat/ | Interface de chat support |

---

## Comptes de démonstration

| Utilisateur | Mot de passe | Rôle |
|-------------|--------------|------|
| admin | CofinanceCI2026! | Administrateur |
| agent_kone | CofinanceCI2026! | Agent |
| cliente_adjoua | CofinanceCI2026! | Client |
| client_kouassi | CofinanceCI2026! | Client |
| cliente_fatou | CofinanceCI2026! | Client |

---
r
## Modules API

| Endpoint | Description |
|----------|-------------|
| /api/accounts/ | Authentification et profils |
| /api/credits/ | Gestion des microcrédits |
| /api/remboursements/ | Suivi des remboursements |
| /api/assurances/ | Produits et souscriptions |
| /api/notifications/ | Notifications in-app |
| /api/support/ | Chat support client |
| /api/dashboard/ | Tableau de bord administrateur |

---

## Démonstration du chat en temps réel

1. Lancer le serveur
2. Ouvrir deux onglets sur http://127.0.0.1:8000/chat/
3. Onglet 1 : se connecter avec `cliente_adjoua`
4. Onglet 2 : se connecter avec `agent_kone`
5. Entrer l'ID de conversation `1` dans les deux onglets
6. Envoyer un message depuis un onglet et observer l'arrivée instantanée dans l'autre

---

## Configuration PostgreSQL (production)

Dans `config/settings.py`, remplacer la section DATABASES :

```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'cofinance_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```