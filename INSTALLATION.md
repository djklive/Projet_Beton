# 📥 Instructions d'Installation - Application Dossier Patient

## Prérequis

Vous devez avoir installé :

1. **Python 3.9 ou plus récent**
   - Télécharger depuis : https://www.python.org/downloads/
   - ✅ **IMPORTANT** : Cocher "Add Python to PATH" lors de l'installation

2. **PostgreSQL**
   - Télécharger depuis : https://www.postgresql.org/download/
   - Installer avec pgAdmin inclus
   - Notez votre **nom d'utilisateur** et **mot de passe** PostgreSQL

---

## 🚀 Installation Étape par Étape

### Étape 1 : Extraire le Fichier ZIP

1. Décompressez `Projet_Patient_Application.zip`
2. Placez le dossier dans un emplacement facile (ex: `C:\Mes_Projets\Projet_Patient\`)

### Étape 2 : Configurer PostgreSQL

1. **Démarrer PostgreSQL**
   - Le service PostgreSQL doit être actif (démarre automatiquement au démarrage de Windows)

2. **Ouvrir pgAdmin**
   - pgAdmin s'ouvre automatiquement après l'installation

3. **Créer la base de données** :
   - Clic droit sur "Databases" (à gauche)
   - "Create" → "Database..."
   - **Nom** : `db_patients`
   - Cliquez sur "Save"

4. **Créer la table** :
   - Clic droit sur `db_patients` → "Query Tool"
   - Ouvrez le fichier `create_table.sql` (dans le dossier du projet)
   - **Copiez tout le contenu** et **collez-le** dans Query Tool
   - Cliquez sur **"Execute"** (ou F5)
   - Vérifiez que la table `dossiers_patients` existe dans le menu de gauche

5. **Ajouter la colonne IMC** :
   - Dans Query Tool, ouvrez `add_column_imc.sql`
   - Exécutez le script (Execute ou F5)

### Étape 3 : Configurer l'Application

1. **Ouvrir le fichier `app.py`** dans un éditeur de texte :
   - Notepad++ (recommandé) : https://notepad-plus-plus.org/
   - VS Code : https://code.visualstudio.com/
   - Ou même le Bloc-notes Windows

2. **Trouver les lignes 22-25** :
   ```python
   POSTGRES_USER = "postgres"
   POSTGRES_PASSWORD = "Djoko002&"
   POSTGRES_HOST = "localhost"
   POSTGRES_PORT = "5432"
   POSTGRES_DB = "db_patients"
   ```

3. **Modifier selon VOS identifiants** :
   ```python
   POSTGRES_USER = "VOTRE_NOM_UTILISATEUR"  # Ex: postgres
   POSTGRES_PASSWORD = "VOTRE_MOT_DE_PASSE"  # Votre mot de passe PostgreSQL
   POSTGRES_HOST = "localhost"  # Ne changez pas
   POSTGRES_PORT = "5432"  # Ne changez pas sauf si vous utilisez un port différent
   POSTGRES_DB = "db_patients"  # Ne changez pas
   ```

4. **Sauvegarder** le fichier (Ctrl+S)

### Étape 4 : Installer les Dépendances Python

1. **Ouvrir PowerShell** dans le dossier du projet :
   - **Méthode 1** : Clic droit dans le dossier (Explorateur Windows) → "Ouvrir dans PowerShell"
   - **Méthode 2** : Tapez `powershell` dans la barre d'adresse de l'Explorateur
   - **Méthode 3** : Ouvrez PowerShell et tapez :
     ```powershell
     cd "chemin\vers\le\dossier"
     ```

2. **Créer un environnement virtuel** :
   ```powershell
   python -m venv venv
   ```
   Cela crée un dossier `venv` (peut prendre 1-2 minutes)

3. **Activer l'environnement virtuel** :
   ```powershell
   .\venv\Scripts\activate
   ```
   Vous devriez voir `(venv)` au début de la ligne de commande

4. **Installer les dépendances** :
   ```powershell
   pip install -r requirements.txt
   ```
   Cela peut prendre 5-10 minutes la première fois (téléchargement des bibliothèques)

### Étape 5 : Lancer l'Application

1. **Assurez-vous que l'environnement virtuel est activé** :
   - Vous devriez voir `(venv)` au début de la ligne
   - Si non, tapez : `.\venv\Scripts\activate`

2. **Lancer l'application** :
   ```powershell
   python app.py
   ```

3. **Ouvrir le navigateur** :
   - Ouvrez votre navigateur (Chrome, Firefox, Edge)
   - Allez à l'adresse : **http://localhost:8000**
   - L'application devrait s'afficher !

---

## ✅ Vérification que Tout Fonctionne

### Test 1 : Enregistrer un Patient

1. Allez sur l'onglet "📝 Saisie Infirmière"
2. Remplissez le formulaire :
   - Référence : PAT-001
   - Date : 01/01/1990
   - Sexe : Homme
   - Poids : 70 kg
   - Taille : 175 cm
   - Tension : 120/80
   - Température : 37.0
3. Cliquez sur "💾 Enregistrer la Visite"
4. **Vérifiez** : Message de succès + IMC affiché

### Test 2 : Vérifier dans pgAdmin

1. Ouvrez pgAdmin
2. Allez dans `db_patients` > `dossiers_patients`
3. Clic droit → "View/Edit Data" → "All Rows"
4. **Vérifiez** : Votre patient devrait être présent

### Test 3 : Voir les Analyses

1. Allez sur l'onglet "📊 Tableau de Bord Médecin"
2. **Vérifiez** :
   - Statistiques globales affichées
   - Graphiques s'affichent
   - Pas d'erreur

---

## 🐛 Résolution de Problèmes

### ❌ Erreur : "Module not found"

**Solution :**
1. Vérifiez que le venv est activé (vous voyez `(venv)`)
2. Réinstallez : `pip install -r requirements.txt`

### ❌ Erreur : "Connection refused" ou "could not connect"

**Solution :**
1. Vérifiez que PostgreSQL est démarré
   - Cherchez "Services" dans Windows
   - Trouvez "postgresql" → Clic droit → "Démarrer"
2. Vérifiez les identifiants dans `app.py`

### ❌ Erreur : "password authentication failed"

**Solution :**
1. Vérifiez vos identifiants PostgreSQL dans `app.py`
2. Testez la connexion dans pgAdmin avec les mêmes identifiants
3. Si votre mot de passe contient des caractères spéciaux (comme `&`), le code les gère automatiquement

### ❌ Erreur : "Table does not exist"

**Solution :**
1. Vérifiez que vous avez bien exécuté `create_table.sql` dans pgAdmin
2. Vérifiez que vous êtes dans la bonne base de données (`db_patients`)

### ❌ Erreur : "Port 8000 already in use"

**Solution :**
1. Fermez toute autre application utilisant le port 8000
2. Ou modifiez le port dans `app.py` (ligne 490 environ) : `app.run(port=8001)`

---

## 📚 Documentation Supplémentaire

Consultez ces fichiers pour plus d'informations :

- **README.md** : Documentation complète du projet
- **Guide_DEMARRAGE.md** : Guide détaillé de démarrage
- **EXPLICATION_ANALYSES.md** : Explication des analyses statistiques
- **DEBUG_GUIDE.md** : Guide de débogage

---

## 🎉 Félicitations !

Votre application est installée et prête à être utilisée !

**Bon développement ! 🚀**

---

## 📞 Besoin d'Aide ?

Si vous rencontrez des problèmes :
1. Consultez d'abord les guides de documentation
2. Vérifiez les messages d'erreur dans la console PowerShell
3. Contactez la personne qui vous a partagé l'application


