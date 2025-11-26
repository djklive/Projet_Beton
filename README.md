# 🏥 Application de Collecte et d'Analyse de Données Patients

Application web développée avec **Shiny for Python**, **PostgreSQL** et des bibliothèques d'analyse de données.

## 📋 Description du Projet

Cette application permet de :
- **Collecter** les données patient via une interface de saisie simple (module Infirmière)
- **Analyser** statistiquement ces données avec des graphiques interactifs (module Médecin)

### Fonctionnalités

#### Module Infirmière (Saisie)
- Formulaire de saisie des signes vitaux
- Calcul automatique de l'IMC (Indice de Masse Corporelle)
- Enregistrement sécurisé dans PostgreSQL
- Validation des données

#### Module Médecin (Analyse)
- **Analyse Univariée** : Distribution des variables (histogrammes, courbes de densité)
- **Analyse Bivariée** : Corrélations entre variables (nuages de points avec régression)
- **Tests Statistiques** : Corrélations de Pearson et Spearman avec interprétation
- Statistiques descriptives (moyenne, médiane, etc.)

## 🛠️ Technologies Utilisées

| Technologie | Version | Rôle |
|-------------|---------|------|
| **Python** | 3.9+ | Langage principal |
| **Shiny for Python** | 1.5.0 | Framework web interactif |
| **PostgreSQL** | Latest | Base de données |
| **pandas** | 2.3.3 | Manipulation de données |
| **SQLAlchemy** | 2.0.44 | ORM pour PostgreSQL |
| **matplotlib** | 3.10.7 | Visualisation |
| **seaborn** | 0.13.2 | Graphiques statistiques |
| **scipy** | Latest | Tests statistiques |

## 📦 Installation

### Prérequis
1. Python 3.9 ou plus récent
2. PostgreSQL installé et configuré
3. pgAdmin (optionnel, pour gestion visuelle)

### Installation des dépendances

1. **Cloner ou télécharger ce projet**

2. **Créer un environnement virtuel** (recommandé)
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**
   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Installer les bibliothèques**
```bash
pip install shiny pandas psycopg2-binary sqlalchemy matplotlib seaborn scipy
```

### Configuration de la base de données

1. **Créer la base de données `db_patients`** dans pgAdmin ou via terminal

2. **Créer la table `dossiers_patients`** :
```sql
CREATE TABLE dossiers_patients (
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
```

3. **Configurer les identifiants PostgreSQL** dans `app.py` :
```python
DATABASE_URL = "postgresql+psycopg2://utilisateur:mot_de_passe@localhost:5432/db_patients"
```

## 🚀 Lancement de l'application

1. **Activer l'environnement virtuel** (voir Installation)

2. **Lancer l'application**
```bash
python app.py
```

Ou avec Shiny :
```bash
shiny run --reload app.py
```

3. **Accéder à l'application**
Ouvrez votre navigateur à l'adresse : `http://localhost:8000`

## 📊 Utilisation

### Module Infirmière
1. Naviguez vers l'onglet "📝 Saisie Infirmière"
2. Remplissez le formulaire avec les données patient
3. L'IMC est calculé automatiquement
4. Cliquez sur "💾 Enregistrer la Visite"

### Module Médecin
1. Naviguez vers l'onglet "📊 Tableau de Bord Médecin"
2. Sélectionnez les variables à analyser dans les menus latéraux
3. Observez les graphiques et les tests statistiques
4. Exportez les résultats si nécessaire

## 🗂️ Structure du Projet

```
Projet/
├── app.py                    # Application principale
├── check_database.sql        # Script SQL de vérification
├── README.md                 # Ce fichier
├── venv/                     # Environnement virtuel Python
└── requirements.txt          # Dépendances (à créer avec pip freeze)
```

## 📈 Analyses Statistiques Implémentées

### Analyse Univariée
- Histogrammes avec courbe de densité (KDE)
- Statistiques descriptives (moyenne, médiane)
- Visualisation de la distribution

### Analyse Bivariée
- Nuages de points avec ligne de régression
- Calcul de corrélations
- Tests statistiques (Pearson, Spearman)

### Variables Disponibles
- Poids (kg)
- Taille (cm)
- IMC (Indice de Masse Corporelle)
- Tension artérielle (systolique et diastolique)
- Température

## 🔐 Sécurité et Conformité

⚠️ **Note importante** : Cette application est destinée à des fins pédagogiques.
Pour un usage en production avec de vraies données patients :
- Implémenter l'authentification utilisateur
- Chiffrer les données sensibles
- Respecter le RGPD/HIPAA
- Ajouter des logs d'audit
- Utiliser HTTPS

## 🤝 Contribution

Ce projet a été développé dans le cadre d'un cours universitaire.

## 📝 License

Projet éducatif - Usage personnel et académique uniquement.

## 🙏 Remerciements

- Shiny for Python par Posit (anciennement RStudio)
- La communauté Python open source
- Les bibliothèques de data science

---

**Développé avec ❤️ en Python**

