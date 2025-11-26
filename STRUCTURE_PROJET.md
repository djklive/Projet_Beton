# 📐 Structure du Projet

## Vue d'ensemble

Ce projet est une **application web interactive** développée avec Shiny for Python pour la collecte et l'analyse de données patients. Elle utilise PostgreSQL comme base de données et intègre des analyses statistiques avancées.

---

## 🗂️ Architecture des Fichiers

```
Projet_Patient/
│
├── 📄 app.py                      # Fichier principal de l'application (408 lignes)
│   ├── UI Infirmière               # Interface de saisie (lignes 29-64)
│   ├── UI Médecin                  # Interface d'analyse (lignes 66-115)
│   └── Logique Serveur             # Fonctions backend (lignes 118-398)
│
├── 📄 requirements.txt             # Dépendances Python
├── 📄 README.md                    # Documentation principale
├── 📄 Guide_DEMARRAGE.md           # Guide de démarrage rapide
├── 📄 STRUCTURE_PROJET.md          # Ce fichier
│
├── 📄 setup_database.py            # Script de vérification de la BDD
├── 📄 check_database.sql           # Script SQL de vérification
├── 📄 config.py.example            # Exemple de configuration
│
└── 📁 venv/                        # Environnement virtuel Python
    ├── Lib/site-packages/          # Bibliothèques installées
    └── Scripts/                    # Scripts d'activation
```

---

## 🗄️ Architecture de la Base de Données

### Table : `dossiers_patients`

```sql
CREATE TABLE dossiers_patients (
    id                      SERIAL PRIMARY KEY,
    patient_ref_id          VARCHAR(100) NOT NULL UNIQUE,
    date_naissance          DATE NOT NULL,
    sexe                    VARCHAR(10) NOT NULL,
    
    -- Données collectées par l'infirmière
    date_visite             TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    poids_kg                NUMERIC(5, 2),
    taille_cm               NUMERIC(5, 1),
    tension_systolique      INTEGER,
    tension_diastolique     INTEGER,
    temperature_celsius     NUMERIC(4, 2),
    
    -- Calculs et annotations
    imc                     NUMERIC(5, 2),          -- Calculé automatiquement
    diagnostic_primaire     TEXT,
    notes_medecin           TEXT
);
```

#### Description des Colonnes

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `id` | SERIAL | Identifiant unique auto-incrémenté | 1, 2, 3... |
| `patient_ref_id` | VARCHAR(100) | Identifiant patient (unique) | PAT-001 |
| `date_naissance` | DATE | Date de naissance | 1990-01-15 |
| `sexe` | VARCHAR(10) | Genre | Homme, Femme, Autre |
| `date_visite` | TIMESTAMP | Date/heure de la visite | 2024-01-20 10:30:00 |
| `poids_kg` | NUMERIC(5,2) | Poids en kilogrammes | 70.50 |
| `taille_cm` | NUMERIC(5,1) | Taille en centimètres | 175.5 |
| `tension_systolique` | INTEGER | Tension artérielle max | 120 |
| `tension_diastolique` | INTEGER | Tension artérielle min | 80 |
| `temperature_celsius` | NUMERIC(4,2) | Température corporelle | 37.50 |
| `imc` | NUMERIC(5,2) | Indice de Masse Corporelle (calculé) | 22.86 |
| `diagnostic_primaire` | TEXT | Diagnostic du médecin | Hypertension |
| `notes_medecin` | TEXT | Notes complémentaires | Notes libres |

---

## 🔄 Flux de Données

### 1. Module Infirmière (Saisie)

```
┌─────────────────┐
│  Interface UI   │
│  (Formulaire)   │
└────────┬────────┘
         │ Remplissage du formulaire
         ↓
┌─────────────────┐
│  Server Logic   │
│  - Validation   │
│  - Calcul IMC   │
└────────┬────────┘
         │ Insertion
         ↓
┌─────────────────┐
│   PostgreSQL    │
│   dossiers_     │
│   patients      │
└─────────────────┘
```

**Fonctionnalités :**
- Formulaire de saisie avec champs obligatoires
- Validation des données côté client
- Calcul automatique de l'IMC
- Enregistrement dans PostgreSQL
- Messages de succès/erreur

### 2. Module Médecin (Analyse)

```
┌─────────────────┐
│  PostgreSQL     │
│  (Données)      │
└────────┬────────┘
         │ Requête SQL
         ↓
┌─────────────────┐
│  Server Logic   │
│  - Chargement   │
│  - Calcul stats │
└────────┬────────┘
         │
         ├──→ Analyse Univariée
         │    (Histogrammes, KDE)
         │
         ├──→ Analyse Bivariée
         │    (Corrélations)
         │
         └──→ Tests Statistiques
              (Pearson, Spearman)
         ↓
┌─────────────────┐
│  Visualisations │
│  (Graphiques)   │
└─────────────────┘
```

**Fonctionnalités :**
- Chargement réactif des données
- Statistiques descriptives
- Graphiques interactifs (matplotlib/seaborn)
- Tests de corrélation avec p-valeurs
- Interprétation automatique

---

## 🎯 Analyses Statistiques

### 1. Analyse Univariée

**Objectif :** Comprendre la distribution d'une variable

**Méthodes :**
- Histogramme avec courbe de densité (KDE)
- Statistiques descriptives :
  - Moyenne
  - Médiane
  - Variance
  - Écart-type

**Variables disponibles :**
- Poids, Taille, IMC
- Tension artérielle (systolique/diastolique)
- Température

### 2. Analyse Bivariée

**Objectif :** Identifier les relations entre deux variables

**Méthodes :**
- Nuage de points (scatter plot)
- Ligne de régression
- Coefficient de corrélation

**Graphiques :**
- Affichage des points de données
- Droite de régression linéaire
- Intervalles de confiance (optionnel)

### 3. Tests de Corrélation

**Tests implémentés :**

| Test | Type de Relation | Usage |
|------|------------------|-------|
| **Pearson** | Linéaire | Deux variables continues, normalité supposée |
| **Spearman** | Monotone | Relation quelconque, non-paramétrique |

**Résultats affichés :**
- Coefficient de corrélation (r ou ρ)
- P-valeur
- Interprétation (force, direction)
- Significativité statistique

---

## 🔧 Technologies et Bibliothèques

### Core
- **Python 3.13** : Langage principal
- **Shiny for Python 1.5.0** : Framework web

### Données
- **pandas 2.3.3** : Manipulation de données
- **SQLAlchemy 2.0.44** : ORM pour PostgreSQL
- **psycopg2-binary 2.9.11** : Driver PostgreSQL

### Statistiques
- **scipy 1.16.3** : Tests statistiques
- **numpy 2.3.4** : Calculs numériques

### Visualisation
- **matplotlib 3.10.7** : Graphiques de base
- **seaborn 0.13.2** : Graphiques statistiques

### Serveur
- **uvicorn 0.38.0** : Serveur ASGI
- **starlette 0.50.0** : Framework web bas niveau
- **websockets 15.0.1** : Communication temps réel

---

## 🚀 Points Forts du Projet

### ✅ Fonctionnalités Complètes
- Interface utilisateur moderne et intuitive
- Navigation par onglets (Infirmière / Médecin)
- Validation des données
- Messages d'erreur clairs

### ✅ Analyses Avancées
- Calculs statistiques robustes
- Visualisations de qualité professionnelle
- Tests statistiques rigoureux
- Interprétation automatique

### ✅ Architecture Solide
- Base de données relationnelle (PostgreSQL)
- Code organisé et modulaire
- Gestion d'erreurs
- Documentation complète

### ✅ Pratiques Professionnelles
- Environnement virtuel isolé
- Gestion des dépendances (requirements.txt)
- Configuration sécurisée
- Guide de démarrage détaillé

---

## 🎓 Objectifs Pédagogiques Atteints

| Objectif | Implémentation |
|----------|----------------|
| **Collecte de données** | Formulaire interactif avec validation |
| **Stockage structuré** | Base PostgreSQL avec schéma défini |
| **Analyse univariée** | Histogrammes, statistiques descriptives |
| **Analyse bivariée** | Nuages de points, corrélations |
| **Tests statistiques** | Pearson, Spearman avec p-valeurs |
| **Visualisation** | Graphiques interactifs et clairs |
| **Application web** | Interface Shiny responsive |

---

## 🔐 Sécurité et Confidentialité

⚠️ **Important :** Application pédagogique

Pour un usage en production :
- [ ] Authentification utilisateur (login/password)
- [ ] Chiffrement des données sensibles
- [ ] HTTPS obligatoire
- [ ] Conformité RGPD/HIPAA
- [ ] Logs d'audit
- [ ] Sauvegarde automatisée
- [ ] Gestion des permissions (rôles)

---

## 📚 Améliorations Futures Possibles

### Court terme
- Export des données (CSV, PDF)
- Filtres avancés par date, sexe, etc.
- Recherche de patients
- Statistiques temporelles

### Moyen terme
- Authentification et gestion des utilisateurs
- Multiples diagnostics par patient
- Histogrammes groupés
- Analyse comparative entre groupes

### Long terme
- Machine Learning (prédictions)
- Alerts automatiques (valeurs anormales)
- Intégration avec systèmes hospitaliers
- Application mobile

---

## 📊 Métriques du Projet

- **Lignes de code** : ~400 (Python)
- **Fichiers** : 8 principaux
- **Dépendances** : 47 packages
- **Modules fonctionnels** : 2 (Infirmière, Médecin)
- **Analyses** : 3 types (univariée, bivariée, tests)
- **Graphiques** : 2 types (histogrammes, scatter plots)

---

**Projet développé avec passion pour l'analyse de données médicales ! 🏥📊**

