# 🗄️ Guide d'Initialisation de la Base de Données sur Railway

Ce guide explique comment initialiser votre base de données PostgreSQL sur Railway.

---

## ⚠️ Problème Commun : Mauvais Répertoire

Si vous obtenez cette erreur :
```
python: can't open file 'C:\\Users\\DELL\\init_db_railway.py': [Errno 2] No such file or directory
```

**C'est parce que vous n'êtes pas dans le bon répertoire !**

---

## ✅ Solution : Naviguer vers le Bon Répertoire

### Étape 1 : Ouvrir PowerShell dans le Bon Dossier

1. Ouvrez l'Explorateur de fichiers Windows
2. Naviguez vers : `C:\Users\DELL\Downloads\Mon site web cour\Python`
3. Cliquez dans la barre d'adresse et tapez `powershell`
4. Appuyez sur Entrée

**OU** dans PowerShell :

```powershell
cd "C:\Users\DELL\Downloads\Mon site web cour\Python"
```

### Étape 2 : Vérifier que les Fichiers Existent

```powershell
dir init_db_railway.py
dir create_table_genie_civil.sql
```

Vous devriez voir ces fichiers listés.

### Étape 3 : Lier le Projet Railway

```powershell
railway link
```

Sélectionnez :
- Workspace : `djklive's Projects`
- Project : `industrious-curiosity`
- Environment : `production`
- Service : **Votre service Python** (pas PostgreSQL !)

**⚠️ IMPORTANT** : Sélectionnez votre **service Python**, pas le service PostgreSQL !

### Étape 4 : Initialiser la Base de Données

```powershell
railway run python init_db_railway.py
```

---

## 🎯 Méthode Alternative : Via un Script SQL Direct

Si `railway run` ne fonctionne pas, utilisez cette méthode :

### Option 1 : Via Railway CLI + psql

1. **Obtenir la DATABASE_URL** :

```powershell
railway variables --output json > railway_vars.json
```

Ouvrez `railway_vars.json` et copiez la valeur de `DATABASE_URL`.

2. **Se connecter à PostgreSQL** :

```powershell
railway connect postgres
```

3. **Dans la console psql, exécutez** :

```sql
-- Copiez-collez le contenu de create_table_genie_civil.sql ici
```

Ou créez un script temporaire :

```powershell
# Se connecter et exécuter le script
railway connect postgres < create_table_genie_civil.sql
```

---

## 🔧 Méthode Alternative : Via l'Interface Railway Web

### Méthode 1 : Via le Service PostgreSQL

1. Dans Railway, cliquez sur votre **service PostgreSQL**
2. Onglet **"Data"** ou **"Query"**
3. Collez le contenu de `create_table_genie_civil.sql`
4. Exécutez la requête

### Méthode 2 : Via un Déploiement Temporaire

Créez un fichier `init_db_one_time.py` :

```python
import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(DATABASE_URL)

with open("create_table_genie_civil.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

with engine.connect() as conn:
    conn.execute(text(sql_script))
    conn.commit()

print("✅ Table créée avec succès!")
```

Puis dans votre `app_genie_civil.py`, ajoutez temporairement au début du fichier `server()` :

```python
# TEMPORAIRE - Supprimer après la première exécution
@reactive.Effect
def init_db_once():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'projets_beton'
                );
            """))
            if not result.fetchone()[0]:
                print("Création de la table...")
                with open("create_table_genie_civil.sql", "r", encoding="utf-8") as f:
                    sql_script = f.read()
                conn.execute(text(sql_script))
                conn.commit()
                print("✅ Table créée!")
    except Exception as e:
        print(f"Erreur: {e}")
```

**⚠️ Supprimez ce code après la première exécution !**

---

## 📋 Checklist Complète

### ✅ Vérifications Préalables

- [ ] Être dans le bon répertoire : `C:\Users\DELL\Downloads\Mon site web cour\Python`
- [ ] Fichiers présents : `init_db_railway.py` et `create_table_genie_civil.sql`
- [ ] Railway CLI installé : `railway --version`
- [ ] Connecté à Railway : `railway login`
- [ ] Projet lié : `railway link` (sélectionner le service **Python**, pas PostgreSQL)

### ✅ Initialisation

- [ ] Méthode choisie (CLI, Web, ou temporaire dans le code)
- [ ] Script SQL exécuté
- [ ] Table `projets_beton` créée
- [ ] Vérification dans Railway ou via `railway connect postgres`

---

## 🔍 Vérifier que la Table Existe

### Via Railway CLI

```powershell
railway connect postgres
```

Puis dans psql :

```sql
\dt
```

Vous devriez voir `projets_beton` listée.

### Via Python dans Railway

```powershell
railway run python -c "from sqlalchemy import create_engine, text; import os; engine = create_engine(os.getenv('DATABASE_URL').replace('postgresql://', 'postgresql+psycopg2://', 1)); conn = engine.connect(); result = conn.execute(text(\"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'projets_beton');\")); print('Table existe:', result.fetchone()[0])"
```

---

## 🎯 Résumé des Commandes (Dans le Bon Répertoire)

```powershell
# 1. Aller dans le bon répertoire
cd "C:\Users\DELL\Downloads\Mon site web cour\Python"

# 2. Vérifier les fichiers
dir init_db_railway.py
dir create_table_genie_civil.sql

# 3. Lier le projet (sélectionner le SERVICE PYTHON)
railway link

# 4. Initialiser la base de données
railway run python init_db_railway.py
```

---

## 🐛 Dépannage

### Erreur : "No such file or directory"

**Solution** : Vérifiez que vous êtes dans le bon répertoire :
```powershell
pwd  # Affiche le répertoire actuel
cd "C:\Users\DELL\Downloads\Mon site web cour\Python"
```

### Erreur : "Project not linked"

**Solution** :
```powershell
railway link
```
**Important** : Sélectionnez le **service Python**, pas PostgreSQL !

### Erreur : "DATABASE_URL not found"

**Solution** : Vérifiez que PostgreSQL est ajouté dans Railway :
1. Service PostgreSQL → Variables
2. Vous devriez voir `DATABASE_URL`

---

## ✅ Méthode la Plus Simple

**Étape par étape** :

1. **Ouvrir PowerShell dans le dossier du projet** :
   - Naviguez vers `C:\Users\DELL\Downloads\Mon site web cour\Python` dans l'explorateur
   - Dans la barre d'adresse, tapez `powershell` et Entrée

2. **Vérifier les fichiers** :
   ```powershell
   ls init_db_railway.py
   ls create_table_genie_civil.sql
   ```

3. **Lier le projet** (sélectionner le SERVICE PYTHON) :
   ```powershell
   railway link
   ```

4. **Initialiser** :
   ```powershell
   railway run python init_db_railway.py
   ```

---

**C'est tout ! 🎉**

Si vous avez encore des problèmes, dites-moi à quelle étape vous bloquez.

