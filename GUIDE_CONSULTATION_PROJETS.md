# 📋 Guide du Module Consultation Projets

## 🎯 Fonctionnalité

Le module **"Consultation Projets"** permet de consulter tous les résultats détaillés de chaque projet enregistré dans la base de données.

---

## 📍 Accès

1. Lancez l'application : `python app_genie_civil.py`
2. Cliquez sur l'onglet **"📋 Consultation Projets"** dans la barre de navigation
3. Le module s'affiche avec :
   - **Menu latéral gauche** : Liste des projets
   - **Zone principale** : Résultats détaillés du projet sélectionné

---

## 🔍 Utilisation

### Étape 1 : Sélectionner un Projet

Dans le menu latéral gauche :
- Un menu déroulant liste **tous les projets** enregistrés
- Chaque projet affiche :
  - Nom du projet
  - Type de structure
  - Volume de béton (m³)
  - Coût total (€)
- Le nombre total de projets est affiché en bas

### Étape 2 : Consulter les Résultats

Une fois un projet sélectionné, **tous les résultats** s'affichent dans la zone principale :

#### 📊 Section 1 : Résultats de Calcul

- **Quantité de Béton** : Volume nécessaire en m³
- **Dimensions des Éléments Structurels** :
  - Poutres (largeur × hauteur)
  - Colonnes (dimensions carrées)
  - Dalles (épaisseur)
  - Structure globale (longueur × largeur × hauteur)
- **Résistance de la Structure** :
  - Résistance du béton
  - Résistance structurelle calculée
  - Type de béton
- **Déplacement et Déformation** :
  - Déformation
  - Déplacement estimé (mm)

#### 💰 Section 2 : Coûts et Planification

- **Détail des Coûts** :
  - Coût des matériaux (ciment, sable, gravier)
  - Total matériaux
  - Coût de la main-d'œuvre
  - **Coût total du projet** (mis en évidence)
- **Durée du Projet** :
  - Durée estimée en jours
  - Basée sur le volume et la productivité

#### ⚖️ Section 3 : Analyse de Sécurité

- Charge totale appliquée (kN)
- Contrainte appliquée (MPa)
- Résistance du béton (MPa)
- **Marge de sécurité** (avec code couleur)
- Coefficient de sécurité requis
- **Alerte visuelle** : ⚠️ si insuffisant, ✅ si acceptable

#### 📦 Section 4 : Quantités de Matériaux

Tableau détaillé avec :
- Ciment (kg)
- Eau (kg)
- Sable (kg)
- Gravier (kg)

#### 📋 Résumé Exécutif

4 cartes visuelles en bas :
- 📐 **Volume** : Volume de béton
- 💰 **Coût Total** : Coût du projet
- 📅 **Durée** : Durée estimée
- ⚠️/✅ **Sécurité** : Statut de sécurité

---

## 🎨 Informations Affichées dans le Menu Latéral

Quand un projet est sélectionné, le menu latéral affiche aussi :
- **Nom du projet**
- **Type de structure**
- **Forme de la structure**
- **Statut** (En conception, Approuvé, etc.)

---

## 🔄 Mise à Jour Automatique

- La liste des projets se met à jour **automatiquement** quand :
  - Un nouveau projet est créé dans l'onglet "Saisie Projet"
  - Vous cliquez sur le bouton de soumission

---

## 📊 Cas d'Utilisation

### Pour la Planification
- Consulter la **durée** de chaque projet
- Comparer les **coûts** entre projets
- Vérifier les **quantités de matériaux** à commander

### Pour la Communication
- Présenter les résultats aux **parties prenantes**
- Exporter les informations (copier depuis l'interface)
- Partager les **résumés exécutifs**

### Pour l'Analyse
- Vérifier la **sécurité** de chaque projet
- Comparer les **dimensions structurelles**
- Analyser les **résistances** calculées

---

## ⚠️ Notes Importantes

### Si Aucun Projet N'Apparaît

- Vérifiez que vous avez créé au moins un projet dans l'onglet "Saisie Projet"
- Vérifiez la connexion à PostgreSQL
- Vérifiez que la table `projets_beton` existe

### Si Certaines Données Manquent

- Les projets créés **avant** l'ajout des nouvelles colonnes peuvent avoir des valeurs `NULL`
- Exécutez `add_columns_resultats.sql` pour ajouter les colonnes manquantes
- Les nouveaux projets auront toutes les données complètes

---

## 🎯 Avantages

✅ **Consultation rapide** : Tous les résultats en un clic  
✅ **Interface claire** : Organisation par sections  
✅ **Résumé visuel** : Cartes pour vue d'ensemble  
✅ **Mise à jour automatique** : Liste toujours à jour  
✅ **Données complètes** : Tous les calculs affichés  

---

## 🚀 Prêt à Utiliser !

Le module est maintenant disponible dans votre application. Testez-le en :
1. Créant un projet dans "Saisie Projet"
2. Allant dans "Consultation Projets"
3. Sélectionnant le projet créé
4. Consultant tous les résultats détaillés

**Profitez de cette nouvelle fonctionnalité ! 📋📊**

