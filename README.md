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
git clone https://github.com/<votre-repo>/cofinance-ci.git
cd cofinance-ci
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

### 6. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 7. Lancer le serveur

```bash
python manage.py runserver
```

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
| admin | (défini à la création) | Administrateur |
| agent_kone | CofinanceCI2026! | Agent |
| cliente_adjoua | CofinanceCI2026! | Client |
| client_kouassi | CofinanceCI2026! | Client |

---

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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cofinance_db',
        'USER': 'postgres',
        'PASSWORD': 'St_connor01',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```