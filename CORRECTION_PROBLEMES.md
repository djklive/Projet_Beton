# 🔧 Guide de Correction des Problèmes

## ✅ Corrections Appliquées dans app.py

### 1. **Colonne IMC manquante**
**Problème :** La table `dossiers_patients` n'a pas la colonne `imc`.

**Solution :** Exécutez le script SQL suivant dans pgAdmin :

```sql
ALTER TABLE dossiers_patients
ADD COLUMN IF NOT EXISTS imc NUMERIC(5, 2);
```

Ou utilisez le fichier `add_column_imc.sql` que j'ai créé.

---

### 2. **Zone de messages qui ne s'affiche pas**
**Problème :** Le cercle de chargement tourne indéfiniment.

**Solution :** ✅ CORRIGÉ
- Remplacement de `.set()` par des variables réactives `reactive.Value()`
- Ajout de fonctions `@render.text` et `@render.ui` pour afficher correctement les messages

---

### 3. **Données qui ne s'enregistrent pas**
**Problème :** Rien ne s'enregistre dans PostgreSQL.

**Solutions appliquées :**
- ✅ Utilisation de `engine.begin()` au lieu de `engine.connect()` + `commit()` (SQLAlchemy 2.0)
- ✅ Ajout de `print()` pour le débogage des erreurs dans la console
- ✅ Meilleure gestion des exceptions

**À vérifier :**
1. Vos identifiants PostgreSQL dans `app.py` ligne 20 sont corrects
2. PostgreSQL est démarré
3. La colonne `imc` existe dans la table (voir point 1)
4. Regardez la console Python pour voir les erreurs détaillées

---

### 4. **Message "Aucune donnée disponible"**
**Problème :** Le module Médecin affiche "Aucune donnée disponible".

**Solution :** ✅ CORRIGÉ
- La fonction `charger_donnees()` se met maintenant à jour automatiquement quand vous enregistrez un patient
- Ajout de `input.submit_btn()` dans la fonction pour déclencher le rechargement

---

## 📋 Étapes à Suivre MAINTENANT

### Étape 1 : Ajouter la colonne IMC (OBLIGATOIRE)

1. Ouvrez **pgAdmin**
2. Connectez-vous à votre serveur PostgreSQL
3. Cliquez sur **Tools** → **Query Tool**
4. Collez et exécutez ce code :

```sql
ALTER TABLE dossiers_patients
ADD COLUMN IF NOT EXISTS imc NUMERIC(5, 2);
```

5. Vérifiez avec :

```sql
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'dossiers_patients';
```

Vous devriez voir la colonne `imc` dans la liste.

---

### Étape 2 : Vérifier vos Identifiants PostgreSQL

Ouvrez `app.py` ligne 20 et vérifiez :

```python
DATABASE_URL = "postgresql+psycopg2://postgres:Djoko002&@localhost:5432/db_patients"
```

**⚠️ ATTENTION :** Si votre mot de passe contient le caractère `&`, il peut causer des problèmes. Essayez de l'échapper ou utilisez une URL encodée.

**Si votre mot de passe contient `&` :**
- Option 1 : Encoder l'URL (remplacer `&` par `%26`)
- Option 2 : Utiliser `urllib.parse.quote_plus()` dans Python

---

### Étape 3 : Redémarrer l'Application

1. Arrêtez l'application actuelle (Ctrl+C)
2. Redémarrez-la :

```powershell
python app.py
```

3. Regardez la console pour voir les messages d'erreur éventuels

---

### Étape 4 : Tester

1. **Onglet "Saisie Infirmière"** :
   - Remplissez le formulaire
   - Cliquez sur "Enregistrer la Visite"
   - **Vérifiez :**
     - Le message de succès s'affiche ✅
     - L'IMC calculé s'affiche ✅
     - Plus de cercle qui tourne indéfiniment ✅

2. **Vérifiez dans pgAdmin** :
   - Faites clic droit sur `dossiers_patients`
   - View/Edit Data → All Rows
   - Vérifiez que les données sont présentes

3. **Onglet "Tableau de Bord Médecin"** :
   - Les données devraient maintenant s'afficher
   - Les graphiques devraient apparaître

---

## 🐛 Si Ça Ne Fonctionne Toujours Pas

### Vérifier les Erreurs dans la Console

Quand vous cliquez sur "Enregistrer", regardez la console Python. Vous devriez voir :
- Soit : `INFO: ...` (succès)
- Soit : `ERREUR DÉTAILLÉE: ...` (erreur)

### Problème de Mot de Passe avec `&`

Si votre mot de passe contient `&` (comme `Djoko002&`), modifiez `app.py` :

```python
from urllib.parse import quote_plus

postgres_user = "postgres"
postgres_password = "Djoko002&"  # Votre mot de passe avec &
postgres_host = "localhost"
postgres_port = "5432"
postgres_db = "db_patients"

# Encoder le mot de passe
encoded_password = quote_plus(postgres_password)

DATABASE_URL = f"postgresql+psycopg2://{postgres_user}:{encoded_password}@{postgres_host}:{postgres_port}/{postgres_db}"
engine = create_engine(DATABASE_URL)
```

---

## 📝 Résumé des Corrections

✅ **app.py corrigé** :
- Variables réactives pour les messages
- Fonctions `@render.text` et `@render.ui`
- Utilisation de `engine.begin()` pour SQLAlchemy 2.0
- Débogage amélioré avec `print()`
- Rechargement automatique des données

✅ **Script SQL créé** : `add_column_imc.sql`

---

## 🎯 Prochaines Étapes

1. ✅ Exécuter le script SQL pour ajouter la colonne `imc`
2. ✅ Vérifier/corriger les identifiants PostgreSQL si nécessaire
3. ✅ Redémarrer l'application
4. ✅ Tester l'enregistrement
5. ✅ Vérifier dans pgAdmin que les données sont bien enregistrées

---

**Bon courage ! 🚀**

