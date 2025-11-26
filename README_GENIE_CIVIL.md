# 🏗️ Application Génie Civil - Gestion de Projets Béton

Application web interactive développée avec **Shiny for Python** et **PostgreSQL** pour la gestion et l'analyse de projets de génie civil en béton.

## 📋 Description du Projet

Cette application permet de :
- **Concevoir** des projets béton avec calculs automatiques (quantités, coûts, sécurité)
- **Analyser** statistiquement les projets (résistance, coûts, charges, corrélations)
- **Optimiser** les choix de conception basés sur des données historiques

### Fonctionnalités

#### Module Ingénieur (Saisie Projet)
- Formulaire de conception complet
- Calcul automatique du volume de béton selon la forme
- Calcul des quantités de matériaux (ciment, eau, sable, gravier)
- Calcul des coûts (matériaux + main-d'œuvre)
- Analyse de sécurité (marge de sécurité, contraintes)
- Validation automatique des paramètres

#### Module Analyste (Tableau de Bord)
- **Analyse Univariée** : Distribution des variables (volume, coût, résistance, etc.)
- **Analyse Bivariée** : Corrélations entre variables (ex: Volume vs Coût)
- **Tests Statistiques** : Corrélations de Pearson et Spearman
- Filtres par type de structure
- Statistiques globales (volume total, coût total, etc.)

---

## 🛠️ Technologies Utilisées

| Technologie | Version | Rôle |
|-------------|---------|------|
| **Python** | 3.9+ | Langage principal |
| **Shiny for Python** | 1.5.0 | Framework web interactif |
| **PostgreSQL** | Latest | Base de données |
| **pandas** | 2.3.3 | Manipulation de données |
| **SQLAlchemy** | 2.0.44 | ORM pour PostgreSQL |
| **numpy** | 2.3.4 | Calculs numériques |
| **matplotlib** | 3.10.7 | Visualisation |
| **seaborn** | 0.13.2 | Graphiques statistiques |
| **scipy** | 1.16.3 | Tests statistiques |

---

## 📦 Installation

### Prérequis
1. Python 3.9 ou plus récent
2. PostgreSQL installé et configuré
3. pgAdmin (optionnel, pour gestion visuelle)

### Installation des dépendances

1. **Créer un environnement virtuel**
```bash
python -m venv venv
```

2. **Activer l'environnement virtuel**
   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Installer les bibliothèques**
```bash
pip install shiny pandas psycopg2-binary sqlalchemy matplotlib seaborn scipy numpy
```

### Configuration de la base de données

1. **Créer la base de données `db_genie_civil`** dans pgAdmin

2. **Créer la table `projets_beton`** :
   - Ouvrez pgAdmin → Query Tool
   - Exécutez le script `create_table_genie_civil.sql`

3. **Configurer les identifiants PostgreSQL** dans `app_genie_civil.py` :
```python
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "votre_mot_de_passe"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB = "db_genie_civil"
```

---

## 🚀 Lancement de l'application

1. **Activer l'environnement virtuel**

2. **Lancer l'application**
```bash
python app_genie_civil.py
```

3. **Accéder à l'application**
Ouvrez votre navigateur à l'adresse : `http://localhost:8000`

---

## 📊 Utilisation

### Module Ingénieur

1. Naviguez vers l'onglet "🏗️ Saisie Projet"
2. Remplissez les informations :
   - **Informations du projet** : Nom, type de structure, forme
   - **Dimensions** : Longueur, largeur, hauteur, épaisseur
   - **Charges** : Statique, dynamique, vent, neige, séisme
   - **Propriétés du béton** : Type, résistance, coefficient de sécurité
   - **Composition** : Dosages des matériaux (kg/m³)
3. Cliquez sur "💾 Calculer et Enregistrer le Projet"
4. **Observez les résultats** :
   - Volume et quantités de matériaux
   - Coûts estimés
   - Analyse de sécurité (marge de sécurité)

### Module Analyste

1. Naviguez vers l'onglet "📊 Tableau de Bord Analyste"
2. Sélectionnez les variables à analyser
3. Observez :
   - Distributions univariées
   - Corrélations bivariées
   - Tests statistiques

---

## 🧮 Calculs Automatiques

### Volume de Béton
- **Rectangulaire** : `longueur × largeur × épaisseur`
- **Circulaire** : `π × (rayon²) × épaisseur`
- **Trapézoïdale** : `((longueur + largeur) / 2) × largeur × épaisseur`
- **Irregulière** : `longueur × largeur × épaisseur × 0.8` (facteur de correction)

### Quantités de Matériaux
- Ciment : `volume × dosage_ciment`
- Eau : `volume × dosage_eau`
- Sable : `volume × dosage_sable`
- Gravier : `volume × dosage_gravier`

### Coûts
- Coût matériaux : `quantité × prix_unitaire`
- Coût main-d'œuvre : `volume × 80 €/m³`
- Coût total : Somme de tous les coûts

### Analyse de Sécurité
- Charge totale : `statique + dynamique + vent + neige + séisme`
- Contrainte : `charge_totale / surface`
- Marge de sécurité : `résistance / contrainte`
- Validation : Marge doit être ≥ coefficient de sécurité

---

## 📈 Analyses Statistiques

### Analyse Univariée
- Distribution des volumes de béton
- Distribution des coûts
- Distribution des résistances
- Identification des valeurs normales et aberrantes

### Analyse Bivariée
- **Volume vs Coût** : Relation attendue positive (plus de volume = plus de coût)
- **Résistance vs Marge de sécurité** : Relation positive
- **Charge vs Contrainte** : Relation linéaire
- **Dimensions vs Volume** : Relations géométriques

### Tests de Corrélation
- **Pearson** : Relations linéaires
- **Spearman** : Relations monotones
- Interprétation avec p-valeurs

---

## 🎯 Exemples d'Utilisation

### Exemple 1 : Projet de Bâtiment
- Type : Bâtiment
- Dimensions : 20m × 15m × 0.25m (épaisseur)
- Volume calculé : 75 m³
- Coût estimé : ~6,000 €

### Exemple 2 : Projet de Pont
- Type : Pont
- Dimensions : 50m × 10m × 0.5m
- Volume calculé : 250 m³
- Charges élevées (véhicules)
- Coût estimé : ~20,000 €

---

## 🔐 Sécurité et Validation

L'application vérifie automatiquement :
- ✅ Marge de sécurité suffisante
- ✅ Contraintes dans les limites acceptables
- ✅ Volumes et quantités cohérents
- ✅ Coûts réalistes

---

## 📚 Documentation

- **README_GENIE_CIVIL.md** : Ce fichier
- **EXPLICATION_ANALYSES.md** : Explication détaillée des analyses
- **create_table_genie_civil.sql** : Script de création de la table

---

## 🎓 Objectifs Pédagogiques

| Objectif | Implémentation |
|----------|----------------|
| Calculs de génie civil | ✅ Volume, quantités, coûts |
| Analyse de sécurité | ✅ Marge de sécurité, contraintes |
| Gestion de projets | ✅ Base de données, historique |
| Analyse statistique | ✅ Corrélations, distributions |
| Visualisation | ✅ Graphiques interactifs |

---

**Développé avec ❤️ en Python pour le génie civil**


