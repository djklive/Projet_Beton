# 🚀 Guide de Déploiement sur Railway

Ce guide vous explique comment déployer votre application Shiny sur Railway.

---

## 📋 Prérequis

1. **Compte Railway** : Créez un compte gratuit sur [railway.app](https://railway.app)
2. **Git** : Installé sur votre machine
3. **Compte GitHub** (recommandé) : Pour versionner votre code

---

## 🔧 Étape 1 : Préparation du Projet

### 1.1 Vérifier les fichiers nécessaires

Assurez-vous d'avoir ces fichiers dans votre projet :

- ✅ `app_genie_civil.py` - Votre application principale
- ✅ `requirements.txt` - Dépendances Python
- ✅ `Procfile` - Commande de démarrage
- ✅ `railway.json` ou `railway.toml` - Configuration Railway
- ✅ `create_table_genie_civil.sql` - Script SQL (pour référence)

### 1.2 Vérifier requirements.txt

Votre fichier `requirements.txt` doit contenir au minimum :

```
shiny
pandas
numpy
sqlalchemy
psycopg2-binary
matplotlib
seaborn
scipy
```

---

## 📦 Étape 2 : Créer un Repository GitHub (Recommandé)

### 2.1 Initialiser Git (si pas déjà fait)

```bash
cd "C:\Users\DELL\Downloads\Mon site web cour\Python"
git init
git add .
git commit -m "Initial commit - Application Génie Civil"
```

### 2.2 Créer un repository sur GitHub

1. Allez sur [github.com](https://github.com)
2. Cliquez sur "New repository"
3. Nommez-le (ex: `app-genie-civil`)
4. **Ne cochez PAS** "Initialize with README"
5. Cliquez sur "Create repository"

### 2.3 Pousser votre code

```bash
git remote add origin https://github.com/VOTRE_USERNAME/app-genie-civil.git
git branch -M main
git push -u origin main
```

**Note** : Pour la sécurité, créez un fichier `.gitignore` pour exclure les fichiers sensibles :

```bash
echo "venv/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
```

---

## 🚂 Étape 3 : Déployer sur Railway

### 3.1 Créer un nouveau projet

1. Connectez-vous à [railway.app](https://railway.app)
2. Cliquez sur **"New Project"**
3. Sélectionnez **"Deploy from GitHub repo"**
4. Autorisez Railway à accéder à votre GitHub
5. Sélectionnez votre repository `app-genie-civil`

### 3.2 Ajouter PostgreSQL

1. Dans votre projet Railway, cliquez sur **"+ New"**
2. Sélectionnez **"Database"** → **"Add PostgreSQL"**
3. Railway créera automatiquement une base PostgreSQL
4. **Notez les informations de connexion** (elles apparaîtront dans les variables d'environnement)

### 3.3 Configurer les variables d'environnement

Railway utilisera automatiquement la variable `DATABASE_URL` créée par le service PostgreSQL.

**Vérifiez que ces variables sont définies :**

- `DATABASE_URL` - Automatiquement créée par Railway PostgreSQL
- `PORT` - Automatiquement définie par Railway (ne pas modifier)

### 3.4 Configurer le service

1. Cliquez sur votre service (celui qui déploie votre code Python)
2. Allez dans l'onglet **"Settings"**
3. Vérifiez que :
   - **Build Command** : (laisser vide, Railway détecte automatiquement)
   - **Start Command** : `python -m shiny run app_genie_civil.py --port $PORT --host 0.0.0.0`

---

## 🗄️ Étape 4 : Initialiser la Base de Données

### 4.1 Obtenir les informations de connexion

1. Dans Railway, cliquez sur votre service **PostgreSQL**
2. Allez dans l'onglet **"Variables"**
3. Copiez la valeur de `DATABASE_URL`

### 4.2 Exécuter le script SQL

**Option A : Via pgAdmin (si installé localement)**

1. Connectez-vous à Railway PostgreSQL avec les identifiants
2. Exécutez le contenu de `create_table_genie_civil.sql`

**Option B : Via Railway CLI**

1. Installez Railway CLI : `npm i -g @railway/cli`
2. Connectez-vous : `railway login`
3. Lien votre projet : `railway link`
4. Connectez-vous à PostgreSQL : `railway connect postgres`
5. Exécutez : `psql < create_table_genie_civil.sql`

**Option C : Via un script Python temporaire**

Créez un fichier `init_db.py` :

```python
from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(DATABASE_URL)

with open("create_table_genie_civil.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

with engine.connect() as conn:
    conn.execute(text(sql_script))
    conn.commit()

print("Base de données initialisée avec succès!")
```

Puis exécutez-le une fois sur Railway (via Railway CLI ou en ajoutant temporairement une commande de démarrage).

---

## 🌐 Étape 5 : Accéder à Votre Application

### 5.1 Générer un domaine

1. Dans Railway, cliquez sur votre service Python
2. Allez dans l'onglet **"Settings"**
3. Cliquez sur **"Generate Domain"**
4. Railway créera un domaine comme : `votre-app.up.railway.app`

### 5.2 Tester l'application

1. Cliquez sur le domaine généré
2. Votre application devrait s'ouvrir dans le navigateur
3. Testez la création d'un projet

---

## 🔒 Étape 6 : Sécurité et Bonnes Pratiques

### 6.1 Variables d'environnement sensibles

Railway stocke automatiquement les secrets dans les variables d'environnement. Ne les commitez jamais dans Git.

### 6.2 Domaine personnalisé (Optionnel)

1. Dans Railway, allez dans **"Settings"** → **"Networking"**
2. Ajoutez votre domaine personnalisé
3. Configurez les enregistrements DNS selon les instructions Railway

### 6.3 Monitoring

Railway fournit des logs en temps réel :
- Cliquez sur votre service
- Onglet **"Deployments"** pour voir les logs
- Onglet **"Metrics"** pour les statistiques

---

## 🐛 Dépannage

### Problème : L'application ne démarre pas

**Vérifiez les logs :**
1. Dans Railway, cliquez sur votre service
2. Onglet **"Deployments"** → Cliquez sur le dernier déploiement
3. Consultez les logs d'erreur

**Causes communes :**
- Port incorrect : Vérifiez que vous utilisez `$PORT`
- Dépendances manquantes : Vérifiez `requirements.txt`
- Erreur de syntaxe : Testez localement d'abord

### Problème : Erreur de connexion PostgreSQL

**Vérifiez :**
1. Que le service PostgreSQL est démarré
2. Que `DATABASE_URL` est bien définie
3. Que la table existe (exécutez `create_table_genie_civil.sql`)

### Problème : L'application se charge mais erreur 500

**Vérifiez les logs Railway** pour voir l'erreur exacte. Souvent :
- Problème de connexion à la base de données
- Variable d'environnement manquante
- Erreur dans le code Python

---

## 📊 Étape 7 : Mises à Jour

### 7.1 Mettre à jour le code

1. Modifiez votre code localement
2. Commitez et poussez sur GitHub :
   ```bash
   git add .
   git commit -m "Description des modifications"
   git push
   ```
3. Railway détectera automatiquement les changements et redéploiera

### 7.2 Voir les déploiements

Dans Railway, onglet **"Deployments"** pour voir l'historique des déploiements.

---

## 💰 Coûts Railway

**Plan Gratuit (Hobby) :**
- $5 de crédit gratuit par mois
- Suffisant pour tester et petites applications
- Auto-pause après inactivité

**Plan Pro :**
- $20/mois
- Pas d'auto-pause
- Plus de ressources

**Note** : PostgreSQL sur Railway est facturé séparément (~$5-10/mois pour une petite base).

---

## ✅ Checklist de Déploiement

- [ ] Compte Railway créé
- [ ] Code poussé sur GitHub
- [ ] Projet Railway créé et lié à GitHub
- [ ] Service PostgreSQL ajouté
- [ ] Variables d'environnement vérifiées
- [ ] Script SQL exécuté (table créée)
- [ ] Application accessible via le domaine Railway
- [ ] Test de création d'un projet réussi

---

## 🎉 Félicitations !

Votre application est maintenant en ligne et accessible partout dans le monde !

**URL de votre application** : `https://votre-app.up.railway.app`

---

## 📞 Support

- **Documentation Railway** : [docs.railway.app](https://docs.railway.app)
- **Discord Railway** : [discord.gg/railway](https://discord.gg/railway)
- **Support Email** : support@railway.app

---

**Bon déploiement ! 🚀**

