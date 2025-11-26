# 🔍 Guide de Débogage - Problèmes d'Enregistrement

## ✅ Améliorations Apportées

J'ai ajouté **beaucoup de messages de débogage** pour identifier exactement où le problème se situe.

---

## 📋 Ce qui a été corrigé/modifié

### 1. **Messages de débogage détaillés**
- ✅ Messages `print()` à chaque étape de l'enregistrement
- ✅ Test de connexion PostgreSQL au démarrage de l'application
- ✅ Vérification automatique de la table et des colonnes
- ✅ Traceback complet en cas d'erreur

### 2. **Amélioration de la fonction d'enregistrement**
- ✅ Utilisation de `@reactive.Effect` avec `@reactive.event`
- ✅ Meilleure gestion des erreurs avec traceback

### 3. **Amélioration du chargement des données**
- ✅ Messages de débogage pour voir ce qui est chargé
- ✅ Affichage du nombre d'enregistrements

---

## 🔍 Instructions de Débogage

### Étape 1 : Redémarrer l'Application

**Arrêtez** l'application actuelle (Ctrl+C) et **redémarrez-la** :

```powershell
python app.py
```

### Étape 2 : Regarder les Messages au Démarrage

Quand vous lancez l'application, vous devriez voir dans la console :

```
🔌 Test de connexion à PostgreSQL...
✅ Connexion PostgreSQL réussie! Version: ...
✅ Table 'dossiers_patients' existe
✅ Colonnes disponibles: [...]
✅ Colonne 'imc' existe
```

**Si vous voyez des erreurs au démarrage**, cela nous dira où est le problème.

### Étape 3 : Cliquer sur "Enregistrer" et Observer la Console

Quand vous cliquez sur le bouton "Enregistrer la Visite", regardez **attentivement** la console Python.

Vous devriez voir :

```
🔄 BOUTON CLIQUE - Début de l'enregistrement...
📊 Données calculées - Poids: 70.0, Taille: 175.0, IMC: 22.86
📦 Données préparées: {...}
💾 Tentative d'écriture dans PostgreSQL...
✅ DONNÉES ENREGISTRÉES AVEC SUCCÈS DANS POSTGRESQL!
📝 Message de succès: ...
📊 IMC affiché: ...
```

**OU** vous verrez une erreur :

```
🔄 BOUTON CLIQUE - Début de l'enregistrement...
❌ ERREUR DÉTAILLÉE: ...
❌ Type d'erreur: ...
❌ Traceback complet:
...
```

---

## 🎯 Diagnostic Basé sur les Messages

### Scénario 1 : Aucun message n'apparaît quand vous cliquez

**Problème :** Le bouton ne déclenche pas la fonction.

**Solutions possibles :**
1. Vérifiez que vous êtes bien dans l'onglet "Saisie Infirmière"
2. Vérifiez que le formulaire est complètement chargé
3. Rechargez la page dans le navigateur (F5)

### Scénario 2 : Vous voyez "BOUTON CLIQUE" mais erreur après

**Problème :** La fonction se déclenche mais il y a une erreur.

**Actions :**
1. **Copiez l'erreur complète** de la console
2. Regardez le type d'erreur :
   - `OperationalError` → Problème de connexion PostgreSQL
   - `ProgrammingError` → Problème SQL (colonne manquante, etc.)
   - `ValueError` → Problème de données (format, etc.)
   - `AttributeError` → Problème dans le code

### Scénario 3 : "DONNÉES ENREGISTRÉES" mais rien dans pgAdmin

**Problème :** La transaction n'est pas commitée ou la base est différente.

**Vérifications :**
1. Vérifiez que vous regardez la bonne base `db_patients`
2. Rafraîchissez la vue dans pgAdmin (F5)
3. Vérifiez que vous n'avez pas plusieurs bases avec le même nom

### Scénario 4 : "Aucune donnée disponible" malgré l'enregistrement

**Problème :** Le chargement ne se déclenche pas ou erreur silencieuse.

**Vérifications :**
1. Regardez les messages "🔄 Chargement des données..." dans la console
2. Vérifiez s'il y a des erreurs de chargement
3. Essayez de recharger la page de l'onglet Médecin

---

## 🐛 Problèmes Courants et Solutions

### Problème : "relation dossiers_patients does not exist"

**Solution :**
Exécutez dans pgAdmin :
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

### Problème : "column imc does not exist"

**Solution :**
```sql
ALTER TABLE dossiers_patients
ADD COLUMN IF NOT EXISTS imc NUMERIC(5, 2);
```

### Problème : "password authentication failed"

**Solution :**
1. Vérifiez vos identifiants dans `app.py` (lignes 21-22)
2. Testez la connexion dans pgAdmin avec les mêmes identifiants
3. Vérifiez que PostgreSQL est démarré

### Problème : "connection refused"

**Solution :**
1. Vérifiez que PostgreSQL est démarré
2. Vérifiez le port (par défaut 5432)
3. Vérifiez que le serveur écoute sur localhost

---

## 📝 Prochaines Étapes

1. ✅ Redémarrez l'application avec les nouveaux messages de débogage
2. ✅ Observez attentivement la console au démarrage
3. ✅ Cliquez sur "Enregistrer" et regardez tous les messages
4. ✅ Copiez-moi les messages d'erreur si vous en avez
5. ✅ Testez dans pgAdmin si les données sont bien enregistrées

---

## 🎯 Messages à Me Fournir

Si le problème persiste, **copiez-moi** :

1. **Les messages au démarrage** (test de connexion)
2. **Les messages quand vous cliquez sur "Enregistrer"**
3. **Toute erreur complète** (traceback)
4. **Le résultat de cette requête SQL** dans pgAdmin :
   ```sql
   SELECT COUNT(*) FROM dossiers_patients;
   SELECT column_name FROM information_schema.columns 
   WHERE table_name = 'dossiers_patients';
   ```

---

**Avec ces messages de débogage, nous allons identifier exactement où est le problème ! 🔍**


