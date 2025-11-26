-- Script pour ajouter les nouvelles colonnes de résultats à la table existante
-- À exécuter dans pgAdmin si la table existe déjà

-- Ajouter les colonnes pour les dimensions structurelles
ALTER TABLE projets_beton
ADD COLUMN IF NOT EXISTS largeur_poutre_m NUMERIC(6, 2),
ADD COLUMN IF NOT EXISTS hauteur_poutre_m NUMERIC(6, 2),
ADD COLUMN IF NOT EXISTS largeur_colonne_m NUMERIC(6, 2),
ADD COLUMN IF NOT EXISTS epaisseur_dalle_m NUMERIC(6, 2);

-- Ajouter les colonnes pour résistance et déformation
ALTER TABLE projets_beton
ADD COLUMN IF NOT EXISTS resistance_structure_mpa NUMERIC(6, 2),
ADD COLUMN IF NOT EXISTS deformation NUMERIC(10, 6),
ADD COLUMN IF NOT EXISTS deplacement_mm NUMERIC(10, 2);

-- Ajouter les colonnes pour planification
ALTER TABLE projets_beton
ADD COLUMN IF NOT EXISTS duree_projet_jours INTEGER,
ADD COLUMN IF NOT EXISTS cout_materiaux_eur NUMERIC(10, 2);

-- Vérifier la structure
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'projets_beton'
ORDER BY ordinal_position;

-- Message de confirmation
SELECT 'Colonnes de résultats ajoutées avec succès !' AS message;


