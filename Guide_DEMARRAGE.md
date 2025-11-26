# 🚀 Guide de Démarrage Rapide

## Étape 1 : Vérifier les Identifiants PostgreSQL

**⚠️ IMPORTANT :** Avant de lancer l'application, vous devez modifier les identifiants PostgreSQL dans le fichier `app.py`.

1. Ouvrez `app.py` dans votre éditeur
2. Trouvez la ligne **20** : 
```python
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/db_patients"
```
3. Remplacez `postgres:postgres` par vos identifiants réels :
   - Utilisateur : votre nom d'utilisateur PostgreSQL
   - Mot de passe : votre mot de passe PostgreSQL

**Exemple :** Si vos identifiants sont `admin:password123`, la ligne devient :
```python
DATABASE_URL = "postgresql+psycopg2://admin:password123@localhost:5432/db_patients"
```

---

## Étape 2 : Vérifier la Base de Données

Assurez-vous que :
1. PostgreSQL est démarré sur votre machine
2. La base de données `db_patients` existe
3. La table `dossiers_patients` est créée avec toutes les colonnes nécessaires

### Pour vérifier/créer la table dans pgAdmin :

1. Ouvrez pgAdmin
2. Connectez-vous à votre serveur PostgreSQL
3. Cliquez sur "Query Tool"
4. Exécutez ce code SQL :

```sql
-- Créer la table si elle n'existe pas
CREATE TABLE IF NOT EXISTS dossiers_patients (
    id SERIAL PRIMARY KEY,
    patient_ref_id VARCHAR(100) NOT NULL UNIQUE,
    date_naissance DATE NOT NULL,
    sexe VARCHAR(10) NOT NULL,
    date_visite TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    poids_kg NUMERIC(5, 2),
    taille_cm NUMERIC(5, 1),
    tension_systolique INTEGER,
    tension_diastolique INTEGER,
    temperature_celsius NUMERIC(4, 2),
    diagnostic_primaire TEXT,
    notes_medecin TEXT,
    imc NUMERIC(5, 2)
);

-- Vérifier la structure
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'dossiers_patients';

-- Ajouter la colonne imc si elle manque
ALTER TABLE dossiers_patients ADD COLUMN IF NOT EXISTS imc NUMERIC(5, 2);
```

---

## Étape 3 : Activer l'Environnement Virtuel

Dans votre terminal PowerShell :

```powershell
# Naviguez vers le dossier du projet
cd "C:\Users\DELL\Downloads\Mon site web cour\Python"

# Activez l'environnement virtuel
.\venv\Scripts\activate

# Vérifiez que vous êtes dans le venv (vous verrez "(venv)" au début)
```

---

## Étape 4 : Lancer l'Application

Une fois l'environnement virtuel activé :

```powershell
# Option 1 : Lancer directement
python app.py

# Option 2 : Lancer avec Shiny (recommandé)
shiny run --reload app.py
```

Vous devriez voir un message indiquant que le serveur démarre sur le port 8000.

---

## Étape 5 : Accéder à l'Application

1. Ouvrez votre navigateur web
2. Allez à l'adresse : **http://localhost:8000**
3. Vous verrez l'interface avec deux onglets :
   - 📝 **Saisie Infirmière** : Pour saisir les données patient
   - 📊 **Tableau de Bord Médecin** : Pour analyser les données

---

## 🐛 Dépannage

### Erreur : "ModuleNotFoundError"
**Solution :** Assurez-vous que l'environnement virtuel est activé et que toutes les bibliothèques sont installées :
```powershell
pip install shiny pandas psycopg2-binary sqlalchemy matplotlib seaborn scipy
```

### Erreur : "Connection refused" ou erreur de connexion à PostgreSQL
**Solution :** 
1. Vérifiez que PostgreSQL est démarré
2. Vérifiez vos identifiants dans `app.py`
3. Vérifiez que le port 5432 est accessible
4. Vérifiez que la base `db_patients` existe

### Erreur : "Port 8000 already in use"
**Solution :** 
1. Fermez toute autre application utilisant le port 8000
2. Ou modifiez le port dans `app.py` (ligne 408 : `app.run(port=8001, reload=True)`)

### Erreur d'encodage (UTF-8)
**Solution :** Cette erreur peut survenir avec des chemins contenant des caractères spéciaux. 
- Essayez de déplacer le projet dans un chemin sans caractères spéciaux
- Ou utilisez un dossier plus simple (ex: `C:\projet_patient`)

---

## ✅ Test Rapide

Pour tester que tout fonctionne :

1. **Lancez l'application** (voir Étape 4)
2. **Allez sur l'onglet "Saisie Infirmière"**
3. **Remplissez le formulaire** :
   - Référence : PAT-001
   - Date de naissance : 1990-01-01
   - Sexe : Homme
   - Poids : 70 kg
   - Taille : 175 cm
   - Tension Systolique : 120
   - Tension Diastolique : 80
   - Température : 37.0

4. **Cliquez sur "Enregistrer la Visite"**
5. **Vérifiez dans pgAdmin** que les données ont été enregistrées
6. **Allez sur l'onglet "Tableau de Bord Médecin"**
7. **Vérifiez** que les graphiques s'affichent correctement

---

## 📚 Ressources

- Documentation Shiny for Python : https://shiny.posit.co/py/
- Documentation PostgreSQL : https://www.postgresql.org/docs/
- Documentation pandas : https://pandas.pydata.org/docs/

---

**Bon développement ! 🎉**

