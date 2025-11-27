# 🔧 Variables d'Environnement pour Railway

Ce guide explique quelles variables d'environnement configurer dans Railway.

---

## ✅ Variables Automatiques (Créées par Railway)

Railway crée automatiquement ces variables pour vous :

### 1. **`DATABASE_URL`** (Automatique si PostgreSQL ajouté)
- **Format** : `postgresql://user:password@host:port/database`
- **Création** : Automatique quand vous ajoutez un service PostgreSQL
- **Où la trouver** :
  1. Dans Railway, cliquez sur votre service **PostgreSQL**
  2. Onglet **"Variables"**
  3. Vous verrez `DATABASE_URL` avec sa valeur

**⚠️ IMPORTANT** : L'application utilise automatiquement cette variable si elle existe. Vous n'avez **PAS besoin** de la créer manuellement !

---

## 🔧 Variables Optionnelles (Pour Configuration Personnalisée)

Si vous n'utilisez **PAS** `DATABASE_URL`, vous pouvez définir ces variables individuellement :

### Configuration PostgreSQL Individuelle

| Variable | Description | Exemple | Obligatoire |
|----------|-------------|---------|-------------|
| `POSTGRES_USER` | Nom d'utilisateur PostgreSQL | `postgres` | Non (défaut: `postgres`) |
| `POSTGRES_PASSWORD` | Mot de passe PostgreSQL | `VotreMotDePasse123` | Non (défaut: local) |
| `POSTGRES_HOST` | Adresse du serveur | `localhost` ou `xxx.railway.app` | Non (défaut: `localhost`) |
| `POSTGRES_PORT` | Port PostgreSQL | `5432` | Non (défaut: `5432`) |
| `POSTGRES_DB` | Nom de la base de données | `db_genie_civil` | Non (défaut: `db_genie_civil`) |

**Note** : En production sur Railway, utilisez `DATABASE_URL` au lieu de ces variables individuelles.

---

## 📝 Comment Ajouter des Variables d'Environnement dans Railway

### Méthode 1 : Via l'Interface Web (Recommandé)

1. **Ouvrez votre projet Railway**
2. **Cliquez sur votre service Python** (celui qui déploie votre application)
3. **Allez dans l'onglet "Variables"**
4. **Cliquez sur "+ New Variable"**
5. **Entrez le nom et la valeur**
6. **Cliquez sur "Add"**

### Méthode 2 : Via Railway CLI

```bash
# Se connecter à Railway
railway login

# Lier votre projet
railway link

# Ajouter une variable
railway variables set POSTGRES_DB=db_genie_civil

# Voir toutes les variables
railway variables
```

---

## 🎯 Configuration Recommandée pour Railway

### ✅ Configuration Simple (Recommandée)

**Une seule variable nécessaire** :

```
DATABASE_URL = (créée automatiquement par Railway PostgreSQL)
```

C'est tout ! Railway gère tout le reste.

---

## 🔍 Vérifier les Variables d'Environnement

### Depuis l'Interface Railway

1. Service Python → **Variables**
2. Toutes les variables disponibles sont listées

### Depuis les Logs de Déploiement

Dans Railway, consultez les logs. Vous verrez :
```
[CONFIG] Utilisation de DATABASE_URL depuis variables d'environnement
```

ou

```
[CONFIG] Utilisation de configuration locale (host: localhost)
```

---

## ⚠️ Bonnes Pratiques

### ✅ À FAIRE

- ✅ Laisser Railway créer `DATABASE_URL` automatiquement
- ✅ Ne jamais commiter les mots de passe dans Git
- ✅ Utiliser les variables d'environnement pour les secrets

### ❌ À ÉVITER

- ❌ Hardcoder les mots de passe dans le code
- ❌ Commiter `.env` avec des secrets dans Git
- ❌ Créer manuellement `DATABASE_URL` si PostgreSQL est déjà ajouté

---

## 🐛 Dépannage

### Problème : "DATABASE_URL not found"

**Solution** :
1. Vérifiez que vous avez ajouté un service PostgreSQL
2. Vérifiez que `DATABASE_URL` apparaît dans les variables du service PostgreSQL
3. Vérifiez que votre service Python peut accéder à ces variables (Railway partage automatiquement)

### Problème : "Connection refused to localhost"

**Solution** :
- L'application utilise encore la configuration locale
- Vérifiez que `DATABASE_URL` est bien définie
- Consultez les logs pour voir quelle configuration est utilisée

### Problème : Variables non partagées entre services

**Solution** :
1. Dans Railway, les variables d'un service PostgreSQL sont automatiquement partagées
2. Si nécessaire, vous pouvez partager manuellement :
   - Service PostgreSQL → Variables → "Share"
   - Sélectionnez le service Python

---

## 📊 Résumé des Variables

| Variable | Automatique ? | Où la trouver | Nécessaire ? |
|----------|---------------|---------------|--------------|
| `DATABASE_URL` | ✅ Oui (si PostgreSQL ajouté) | Service PostgreSQL → Variables | ✅ Oui |
| `PORT` | ✅ Oui | Railway gère automatiquement | ✅ Oui |
| `POSTGRES_USER` | ❌ Non | À définir manuellement | ❌ Non |
| `POSTGRES_PASSWORD` | ❌ Non | À définir manuellement | ❌ Non |
| `POSTGRES_HOST` | ❌ Non | À définir manuellement | ❌ Non |
| `POSTGRES_PORT` | ❌ Non | À définir manuellement | ❌ Non |
| `POSTGRES_DB` | ❌ Non | À définir manuellement | ❌ Non |

---

## 🎉 Configuration Minimale

Pour Railway, vous avez besoin de **ZÉRO variable à configurer manuellement** si vous utilisez PostgreSQL Railway !

1. ✅ Ajoutez PostgreSQL → `DATABASE_URL` créée automatiquement
2. ✅ Railway partage `DATABASE_URL` avec votre service Python
3. ✅ Votre application l'utilise automatiquement

C'est tout ! 🚀

---

**Besoin d'aide ?** Consultez les logs de déploiement dans Railway pour voir quelle configuration est utilisée.

