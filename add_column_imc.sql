-- Script pour ajouter la colonne IMC à la table existante
-- À exécuter dans pgAdmin : Tools > Query Tool

-- Ajouter la colonne imc si elle n'existe pas
ALTER TABLE dossiers_patients
ADD COLUMN IF NOT EXISTS imc NUMERIC(5, 2);

-- Vérifier la structure de la table
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'dossiers_patients'
ORDER BY ordinal_position;

-- Message de confirmation
SELECT 'Colonne imc ajoutée avec succès !' AS message;

