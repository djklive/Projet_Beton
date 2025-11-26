# 🔄 Guide de Migration - Médecine vers Génie Civil

## 📋 Vue d'Ensemble

Ce guide explique comment passer de l'application **médecine** à l'application **génie civil**.

---

## 🎯 Changements Principaux

### Ancienne Application (Médecine)
- Base de données : `db_patients`
- Table : `dossiers_patients`
- Module : Infirmière / Médecin
- Variables : Poids, Taille, Tension, Température, IMC

### Nouvelle Application (Génie Civil)
- Base de données : `db_genie_civil`
- Table : `projets_beton`
- Module : Ingénieur / Analyste
- Variables : Dimensions, Charges, Résistance, Coûts, Volume

---

## 📦 Fichiers à Utiliser

### ✅ **Nouveaux Fichiers (Génie Civil)**
- `app_genie_civil.py` : Application principale
- `create_table_genie_civil.sql` : Script de création de table
- `README_GENIE_CIVIL.md` : Documentation

### ❌ **Anciens Fichiers (Médecine) - À Conserver pour Référence**
- `app.py` : Ancienne application médecine
- `create_table.sql` : Ancienne table patients

---

## 🚀 Installation de la Nouvelle Application

### Étape 1 : Créer la Nouvelle Base de Données

1. Ouvrez **pgAdmin**
2. Clic droit sur "Databases" → "Create" → "Database..."
3. Nom : `db_genie_civil`
4. Cliquez sur "Save"

### Étape 2 : Créer la Table

1. Clic droit sur `db_genie_civil` → "Query Tool"
2. Ouvrez le fichier `create_table_genie_civil.sql`
3. Copiez tout le contenu et exécutez (F5)
4. Vérifiez que la table `projets_beton` existe

### Étape 3 : Configurer l'Application

1. Ouvrez `app_genie_civil.py`
2. Modifiez les identifiants PostgreSQL (lignes 22-26) :
```python
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "votre_mot_de_passe"
POSTGRES_DB = "db_genie_civil"  # Nouvelle base
```

### Étape 4 : Lancer l'Application

```powershell
python app_genie_civil.py
```

---

## 🔄 Option : Garder les Deux Applications

Vous pouvez garder **les deux applications** en parallèle :

1. **Application Médecine** : `app.py` → Port 8000
2. **Application Génie Civil** : `app_genie_civil.py` → Port 8001

Pour changer le port dans `app_genie_civil.py` :
```python
app.run(port=8001, reload=False)  # Ligne ~705
```

---

## 📊 Comparaison des Fonctionnalités

| Fonctionnalité | Médecine | Génie Civil |
|----------------|----------|-------------|
| **Saisie** | Données patient | Projet béton |
| **Calculs** | IMC | Volume, Coûts, Sécurité |
| **Analyses** | Corrélations médicales | Corrélations techniques |
| **Variables** | Poids, Taille, Tension | Dimensions, Charges, Résistance |

---

## 🎓 Avantages de la Nouvelle Application

✅ **Calculs automatiques** : Volume, quantités, coûts
✅ **Analyse de sécurité** : Marge de sécurité automatique
✅ **Gestion de projets** : Historique complet
✅ **Optimisation** : Analyses statistiques pour optimiser les projets futurs

---

## 📝 Notes Importantes

- Les deux applications utilisent les **mêmes bibliothèques Python**
- Les deux utilisent **PostgreSQL** (bases différentes)
- Vous pouvez **copier les dépendances** de `requirements.txt` existant
- Les **analyses statistiques** sont similaires mais adaptées au contexte

---

**Bonne migration ! 🚀**


