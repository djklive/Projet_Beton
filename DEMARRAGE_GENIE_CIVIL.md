# 🚀 Guide de Démarrage Rapide - Application Génie Civil

## ✅ Application Créée avec Succès !

Votre nouvelle application de **Génie Civil** est prête ! 🏗️

---

## 📋 Fichiers Créés

1. **`app_genie_civil.py`** : Application principale (705 lignes)
2. **`create_table_genie_civil.sql`** : Script de création de la table
3. **`README_GENIE_CIVIL.md`** : Documentation complète
4. **`GUIDE_MIGRATION.md`** : Guide de migration depuis médecine

---

## 🚀 Démarrage Rapide (3 Étapes)

### Étape 1 : Créer la Base de Données

1. Ouvrez **pgAdmin**
2. Clic droit sur "Databases" → "Create" → "Database..."
3. Nom : **`db_genie_civil`**
4. Cliquez sur "Save"

### Étape 2 : Créer la Table

1. Clic droit sur `db_genie_civil` → "Query Tool"
2. Ouvrez `create_table_genie_civil.sql`
3. Copiez tout le contenu et exécutez (F5)
4. ✅ Vérifiez que la table `projets_beton` existe

### Étape 3 : Configurer et Lancer

1. Ouvrez `app_genie_civil.py`
2. Modifiez les identifiants PostgreSQL (lignes 22-26)
3. Lancez :
```powershell
python app_genie_civil.py
```
4. Ouvrez : **http://localhost:8000**

---

## 🎯 Test Rapide

### Test 1 : Créer un Projet

1. Allez sur "🏗️ Saisie Projet"
2. Remplissez :
   - Nom : "Projet Test"
   - Type : Bâtiment
   - Dimensions : 10m × 5m × 0.2m
   - Charges : 100 kN statique
   - Résistance : 25 MPa
3. Cliquez sur "Calculer et Enregistrer"
4. ✅ Vérifiez les résultats affichés

### Test 2 : Voir les Analyses

1. Allez sur "📊 Tableau de Bord Analyste"
2. Sélectionnez des variables
3. ✅ Vérifiez que les graphiques s'affichent

---

## 🎓 Fonctionnalités Principales

### Module Ingénieur

✅ **Calculs Automatiques** :
- Volume de béton (selon la forme)
- Quantités de matériaux
- Coûts (matériaux + main-d'œuvre)
- Marge de sécurité

✅ **Validation** :
- Vérification de la marge de sécurité
- Alertes si insuffisant

### Module Analyste

✅ **Analyses** :
- Distribution des volumes
- Distribution des coûts
- Corrélations (Volume vs Coût, etc.)
- Tests statistiques

---

## 📊 Exemples de Projets

### Projet 1 : Fondation de Bâtiment
- Type : Fondation
- Dimensions : 15m × 10m × 0.3m
- Volume : 45 m³
- Coût : ~3,600 €

### Projet 2 : Pont Routier
- Type : Pont
- Dimensions : 50m × 12m × 0.5m
- Volume : 300 m³
- Charges élevées
- Coût : ~24,000 €

---

## 🔧 Personnalisation

### Modifier les Prix des Matériaux

Dans `app_genie_civil.py` (lignes 73-76) :
```python
PRIX_CIMENT = 0.15  # €/kg
PRIX_SABLE = 0.05   # €/kg
PRIX_GRAVIER = 0.04 # €/kg
PRIX_MAIN_OEUVRE = 80  # €/m³
```

### Ajouter de Nouveaux Types de Structures

Dans la section UI (ligne ~50) :
```python
ui.input_select(
    "type_structure",
    "Type de Structure",
    {
        "Bâtiment": "Bâtiment",
        "Votre Nouveau Type": "Votre Nouveau Type",  # Ajoutez ici
        ...
    }
)
```

---

## 🎉 Prêt à Utiliser !

Votre application est **100% fonctionnelle** et prête pour :
- ✅ La conception de projets béton
- ✅ Les calculs automatiques
- ✅ L'analyse statistique
- ✅ L'optimisation des projets

**Bon développement ! 🏗️🚀**


