# 🖥️ Guide Railway CLI

Ce guide explique comment utiliser Railway CLI pour gérer votre projet.

---

## 📥 Installation Railway CLI

### Option 1 : Via npm (Recommandé)

```bash
npm install -g @railway/cli
```

### Option 2 : Via PowerShell (Windows)

```powershell
# Télécharger et installer Railway CLI
iwr https://railway.app/install.ps1 | iex
```

### Option 3 : Via Winget (Windows)

```powershell
winget install --id Railway.RailwayCLI
```

---

## 🔐 Se Connecter à Railway

### Dans PowerShell ou CMD

```powershell
railway login
```

Une page s'ouvrira dans votre navigateur pour vous connecter.

---

## 📂 Lier Votre Projet Local

```powershell
cd "C:\Users\DELL\Downloads\Mon site web cour\Python"
railway link
```

Railway vous demandera de sélectionner un projet existant ou d'en créer un nouveau.

---

## 🗄️ Gérer la Base de Données PostgreSQL

### Se Connecter à PostgreSQL

```powershell
railway connect postgres
```

Cela ouvre une session `psql` connectée à votre base PostgreSQL Railway.

### Exécuter le Script SQL

Une fois connecté, vous pouvez exécuter :

```sql
-- Copier le contenu de create_table_genie_civil.sql
-- Et le coller dans la console psql
```

**Ou depuis PowerShell** (si psql est installé localement) :

```powershell
# Obtenir la DATABASE_URL
railway variables

# Se connecter directement
$DATABASE_URL = railway variables --output json | ConvertFrom-Json | Select-Object -ExpandProperty DATABASE_URL
psql $DATABASE_URL -f create_table_genie_civil.sql
```

### Alternative : Utiliser un Script Python Temporaire

Créez `init_db_railway.py` :

```python
import os
from sqlalchemy import create_engine, text

# Railway CLI fournit les variables d'environnement
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(DATABASE_URL)

with open("create_table_genie_civil.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

with engine.connect() as conn:
    conn.execute(text(sql_script))
    conn.commit()

print("✅ Base de données initialisée!")
```

Exécutez :

```powershell
railway run python init_db_railway.py
```

---

## 🔧 Gérer les Variables d'Environnement

### Voir Toutes les Variables

```powershell
railway variables
```

### Ajouter une Variable

```powershell
railway variables set POSTGRES_DB=db_genie_civil
```

### Supprimer une Variable

```powershell
railway variables unset POSTGRES_DB
```

### Voir une Variable Spécifique

```powershell
railway variables get DATABASE_URL
```

---

## 📊 Voir les Logs

### Logs en Temps Réel

```powershell
railway logs
```

### Logs d'un Service Spécifique

```powershell
railway logs --service nom-du-service
```

---

## 🚀 Commandes Utiles

### Voir le Statut du Projet

```powershell
railway status
```

### Ouvrir le Dashboard dans le Navigateur

```powershell
railway open
```

### Redémarrer un Service

```powershell
railway restart
```

### Voir les Informations du Projet

```powershell
railway whoami
railway project
```

---

## 💻 Utiliser PowerShell vs CMD

### PowerShell (Recommandé)

Railway CLI fonctionne parfaitement dans PowerShell. Utilisez-le de préférence.

### CMD

Railway CLI fonctionne aussi dans CMD, mais PowerShell offre plus de fonctionnalités.

---

## 🔍 Dépannage Railway CLI

### Problème : "railway: command not found"

**Solution** :
- Vérifiez l'installation : `npm list -g @railway/cli`
- Ajoutez npm au PATH si nécessaire
- Réinstallez : `npm install -g @railway/cli`

### Problème : "Error: Not authenticated"

**Solution** :
```powershell
railway login
```

### Problème : "No project linked"

**Solution** :
```powershell
railway link
```

---

## 📝 Workflow Typique

### 1. Se Connecter

```powershell
railway login
```

### 2. Lier le Projet

```powershell
cd "C:\Users\DELL\Downloads\Mon site web cour\Python"
railway link
```

### 3. Initialiser la Base de Données

```powershell
railway run python init_db_railway.py
```

### 4. Vérifier les Variables

```powershell
railway variables
```

### 5. Voir les Logs

```powershell
railway logs
```

---

## 🎯 Commandes Essentielles

| Commande | Description |
|----------|-------------|
| `railway login` | Se connecter à Railway |
| `railway link` | Lier le projet local |
| `railway variables` | Voir les variables |
| `railway logs` | Voir les logs |
| `railway connect postgres` | Se connecter à PostgreSQL |
| `railway run <command>` | Exécuter une commande dans l'environnement Railway |
| `railway open` | Ouvrir le dashboard |

---

## 🎉 Prêt à Utiliser !

Maintenant vous pouvez gérer votre projet Railway depuis la ligne de commande.

**Besoin d'aide ?** Tapez `railway --help` pour voir toutes les commandes disponibles.

