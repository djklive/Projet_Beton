# 📦 Guide de Partage de l'Application

## 🎯 Comment Partager Votre Application avec Votre Ami

Voici comment préparer votre application pour la partager de manière professionnelle.

---

## 📋 Ce Qu'il Faut Partager

### ✅ **À INCLURE dans le package :**

1. **Tous les fichiers Python** (`.py`)
2. **Fichiers SQL** (`.sql`)
3. **Documentation** (`.md`, `.txt`)
4. **Scripts de lancement** (`.bat`)
5. **requirements.txt** (dépendances)

### ❌ **À EXCLURE du package :**

1. **Le dossier `venv/`** (environnement virtuel - trop volumineux)
2. **Fichiers `__pycache__/`** (cache Python)
3. **Fichiers temporaires** (`.pyc`, `.pyo`)

---

## 📦 Étape 1 : Préparer le Dossier à Partager

### Option A : Création Manuelle (Recommandée)

1. **Créez un nouveau dossier** nommé `Projet_Patient_Distribution`

2. **Copiez ces fichiers** dans le nouveau dossier :
   ```
   ✅ app.py
   ✅ requirements.txt
   ✅ create_table.sql
   ✅ add_column_imc.sql
   ✅ check_database.sql
   ✅ README.md
   ✅ Guide_DEMARRAGE.md
   ✅ LANCER.bat
   ✅ config.py.example
   ✅ INSTRUCTIONS_FINALES.txt
   ✅ STRUCTURE_PROJET.md
   ```

3. **Créez un fichier `INSTALLATION.md`** avec les instructions (voir ci-dessous)

### Option B : Script Automatique

Créez un fichier `preparer_partage.bat` :
```batch
@echo off
echo Preparation du package pour partage...

REM Creer le dossier de distribution
mkdir Projet_Patient_Distribution 2>nul

REM Copier les fichiers necessaires
copy app.py Projet_Patient_Distribution\
copy requirements.txt Projet_Patient_Distribution\
copy *.sql Projet_Patient_Distribution\
copy *.md Projet_Patient_Distribution\
copy *.txt Projet_Patient_Distribution\
copy *.bat Projet_Patient_Distribution\
copy config.py.example Projet_Patient_Distribution\

echo.
echo Package prepare dans: Projet_Patient_Distribution\
echo Vous pouvez maintenant compresser ce dossier et le partager!
pause
```

---

## 📦 Étape 2 : Compresser le Dossier

### Méthode 1 : Windows Explorer

1. **Clic droit** sur le dossier `Projet_Patient_Distribution`
2. **Envoyer vers** > **Dossier compressé**
3. Un fichier `.zip` sera créé
4. **Renommez-le** : `Projet_Patient_Application.zip`

### Méthode 2 : PowerShell

```powershell
Compress-Archive -Path "Projet_Patient_Distribution" -DestinationPath "Projet_Patient_Application.zip"
```

---

## 📧 Étape 3 : Partager

### Options de Partage :

1. **Email** : Si le fichier fait moins de 25 MB
2. **Google Drive / OneDrive** : Pour fichiers plus volumineux
3. **GitHub** : Pour partage professionnel (gratuit)
4. **USB** : Transfert direct

---

## 📋 Instructions pour Votre Ami

Créez un fichier `INSTALLATION.md` avec ces instructions :

---

# 📥 Instructions d'Installation - Application Dossier Patient

## Prérequis

Votre ami doit avoir installé :

1. **Python 3.9 ou plus récent**
   - Télécharger depuis : https://www.python.org/downloads/
   - ✅ Cocher "Add Python to PATH" lors de l'installation

2. **PostgreSQL**
   - Télécharger depuis : https://www.postgresql.org/download/
   - Installer avec pgAdmin inclus

3. **Git** (optionnel, pour cloner depuis GitHub)

---

## 🚀 Installation

### Étape 1 : Extraire le Fichier ZIP

1. Décompressez `Projet_Patient_Application.zip`
2. Placez le dossier dans un emplacement facile (ex: `C:\Mes_Projets\`)

### Étape 2 : Configurer PostgreSQL

1. **Démarrer PostgreSQL** (service Windows doit être actif)

2. **Ouvrir pgAdmin**

3. **Créer la base de données** :
   - Clic droit sur "Databases" → "Create" → "Database..."
   - Nom : `db_patients`
   - Cliquez sur "Save"

4. **Créer la table** :
   - Clic droit sur `db_patients` → "Query Tool"
   - Ouvrez le fichier `create_table.sql`
   - Copiez tout le contenu et exécutez (F5)
   - Vérifiez que la table `dossiers_patients` existe

5. **Ajouter la colonne IMC** :
   - Dans Query Tool, ouvrez `add_column_imc.sql`
   - Exécutez le script

### Étape 3 : Configurer l'Application

1. **Ouvrir le fichier `app.py`** dans un éditeur de texte (Notepad++, VS Code, etc.)

2. **Modifier les identifiants PostgreSQL** (lignes 22-25) :
   ```python
   POSTGRES_USER = "postgres"  # Son nom d'utilisateur PostgreSQL
   POSTGRES_PASSWORD = "SON_MOT_DE_PASSE"  # Son mot de passe PostgreSQL
   POSTGRES_HOST = "localhost"
   POSTGRES_PORT = "5432"
   POSTGRES_DB = "db_patients"
   ```

3. **Sauvegarder** le fichier

### Étape 4 : Installer les Dépendances Python

1. **Ouvrir PowerShell** dans le dossier du projet :
   - Clic droit dans le dossier → "Ouvrir dans PowerShell"
   - Ou tapez `cd chemin\vers\le\dossier` dans PowerShell

2. **Créer un environnement virtuel** :
   ```powershell
   python -m venv venv
   ```

3. **Activer l'environnement virtuel** :
   ```powershell
   .\venv\Scripts\activate
   ```
   Vous devriez voir `(venv)` au début de la ligne

4. **Installer les dépendances** :
   ```powershell
   pip install -r requirements.txt
   ```

### Étape 5 : Lancer l'Application

1. **Activer l'environnement virtuel** (si pas déjà fait) :
   ```powershell
   .\venv\Scripts\activate
   ```

2. **Lancer l'application** :
   ```powershell
   python app.py
   ```

3. **Ouvrir le navigateur** :
   - URL : `http://localhost:8000`
   - L'application devrait s'afficher !

---

## ✅ Vérification

1. Testez l'enregistrement d'un patient
2. Vérifiez dans pgAdmin que les données sont présentes
3. Testez les graphiques dans le Tableau de Bord Médecin

---

## 🐛 Problèmes Courants

### Erreur : "Module not found"
**Solution :** Activez le venv et réinstallez : `pip install -r requirements.txt`

### Erreur : "Connection refused"
**Solution :** Vérifiez que PostgreSQL est démarré

### Erreur : "password authentication failed"
**Solution :** Vérifiez les identifiants dans `app.py`

---

## 📞 Support

Consultez les fichiers :
- `Guide_DEMARRAGE.md` : Instructions détaillées
- `README.md` : Documentation complète
- `DEBUG_GUIDE.md` : Résolution de problèmes

---

**Bon développement ! 🚀**


