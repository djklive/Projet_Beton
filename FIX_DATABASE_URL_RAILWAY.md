# 🔧 Fix : DATABASE_URL Non Utilisée sur Railway

## ❌ Problème Identifié

Les logs montrent :
```
[CONFIG] Utilisation de configuration locale (host: localhost)
[INIT] DATABASE_URL configurée: Oui
[DB] ⚠️ Erreur de connexion (non bloquant): connection to server at "localhost" failed
```

**Cause** : `DATABASE_URL` de Railway n'est pas correctement détectée ou partagée avec le service Python.

---

## ✅ Solutions

### Solution 1 : Vérifier le Partage de Variables dans Railway

Railway ne partage **pas automatiquement** `DATABASE_URL` entre services. Il faut le faire manuellement.

#### Étape 1 : Vérifier DATABASE_URL dans le Service PostgreSQL

1. Dans Railway, cliquez sur votre service **PostgreSQL**
2. Onglet **"Variables"**
3. Vérifiez que `DATABASE_URL` existe
4. **Copiez sa valeur** (vous en aurez besoin)

#### Étape 2 : Partager DATABASE_URL avec le Service Python

1. Dans Railway, cliquez sur votre service **PostgreSQL**
2. Onglet **"Variables"**
3. Trouvez `DATABASE_URL`
4. Cliquez sur **"Share"** ou **"..."** → **"Share Variable"**
5. Sélectionnez votre service **Projet_Beton** (service Python)
6. Cliquez sur **"Share"**

**OU** Ajoutez-la manuellement au service Python :

1. Cliquez sur votre service **Projet_Beton** (service Python)
2. Onglet **"Variables"**
3. Cliquez sur **"+ New Variable"**
4. Nom : `DATABASE_URL`
5. Valeur : Copiez la valeur depuis le service PostgreSQL
6. Cliquez sur **"Add"**

---

### Solution 2 : Utiliser le Nom de Variable Railway Spécifique

Railway peut utiliser un nom différent. Essayez aussi :

1. Dans votre service **Projet_Beton** → **Variables**
2. Vérifiez s'il existe une variable comme :
   - `POSTGRES_URL`
   - `PGDATABASE`
   - `DATABASE_URL` (du service PostgreSQL)

---

### Solution 3 : Vérifier via Railway CLI

```powershell
railway variables
```

Cela affichera toutes les variables disponibles. Vérifiez si `DATABASE_URL` est listée.

Si elle n'est pas là, ajoutez-la :

```powershell
# D'abord, obtenir DATABASE_URL du service PostgreSQL
railway variables --service postgres

# Puis l'ajouter au service Python (remplacez SERVICE_NAME par le nom de votre service Python)
railway variables set DATABASE_URL="valeur_copiée" --service SERVICE_NAME
```

---

## 🔍 Debug : Vérifier les Variables d'Environnement

Le code a été amélioré pour afficher plus d'informations. Après le redéploiement, vous devriez voir dans les logs :

```
[CONFIG] DATABASE_URL trouvée (longueur: XXX caractères)
[CONFIG] DATABASE_URL commence par: postgresql://...
[CONFIG] ✅ Utilisation de DATABASE_URL depuis variables d'environnement Railway
```

**OU** si elle n'est pas trouvée :

```
[CONFIG] ⚠️ DATABASE_URL non trouvée, utilisation de la configuration locale
```

---

## 📋 Checklist de Vérification

- [ ] Service PostgreSQL créé dans Railway
- [ ] `DATABASE_URL` existe dans les variables du service PostgreSQL
- [ ] `DATABASE_URL` est partagée avec le service Python OU ajoutée manuellement
- [ ] Code mis à jour avec les améliorations de debug
- [ ] Application redéployée
- [ ] Logs vérifiés pour confirmer l'utilisation de `DATABASE_URL`

---

## 🎯 Solution Rapide (Recommandée)

1. **Dans Railway** :
   - Service PostgreSQL → Variables → Copier `DATABASE_URL`
   - Service Projet_Beton → Variables → "+ New Variable"
   - Nom : `DATABASE_URL`
   - Valeur : Coller la valeur copiée
   - Cliquer sur "Add"

2. **Redéployer** :
   - Railway redéploiera automatiquement, OU
   - Faire un commit/push pour forcer le redéploiement

3. **Vérifier les logs** :
   - Vous devriez maintenant voir :
     ```
     [CONFIG] ✅ Utilisation de DATABASE_URL depuis variables d'environnement Railway
     [DB] Connexion PostgreSQL réussie!
     ```

---

## 🐛 Si PostgreSQL est en "Sleeping"

Si votre service PostgreSQL est en mode "sleeping" (inactif) :

1. **Dans Railway**, cliquez sur votre service PostgreSQL
2. Il devrait se réveiller automatiquement lors de la première connexion
3. Si ce n'est pas le cas, cliquez sur **"Restart"** ou **"Wake Up"**

**Note** : Sur le plan gratuit, Railway met les services en veille après inactivité. La première connexion peut prendre quelques secondes.

---

## ✅ Après Correction

Une fois `DATABASE_URL` correctement configurée, vous devriez voir :

```
[CONFIG] ✅ Utilisation de DATABASE_URL depuis variables d'environnement Railway
[DB] Connexion PostgreSQL réussie! Version: ...
[DB] Table 'projets_beton' n'existe pas. Création en cours...
[DB] ✅ Table 'projets_beton' créée avec succès!
```

---

**Le problème principal est que Railway ne partage pas automatiquement les variables entre services. Il faut le faire manuellement !** 🔧

