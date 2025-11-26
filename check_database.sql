-- Script de vérification et modification de la table dossiers_patients
-- À exécuter dans pgAdmin

-- 1. Vérifier la structure actuelle de la table
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'dossiers_patients';

-- 2. Ajouter la colonne IMC si elle n'existe pas déjà
-- (À exécuter seulement si la colonne n'existe pas)
ALTER TABLE dossiers_patients
ADD COLUMN IF NOT EXISTS imc NUMERIC(5, 2);

-- 3. Afficher tous les enregistrements actuels
SELECT * FROM dossiers_patients;

