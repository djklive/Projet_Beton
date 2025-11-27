-- Script pour ajouter les colonnes manquantes à la table projets_beton
-- À exécuter dans Railway PostgreSQL si les colonnes id et date_creation manquent

-- Ajouter la colonne id si elle n'existe pas
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'projets_beton' AND column_name = 'id'
    ) THEN
        -- Ajouter la colonne id avec SERIAL
        ALTER TABLE projets_beton ADD COLUMN id SERIAL PRIMARY KEY;
        RAISE NOTICE 'Colonne id ajoutée';
    ELSE
        RAISE NOTICE 'Colonne id existe déjà';
    END IF;
END $$;

-- Ajouter la colonne date_creation si elle n'existe pas
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'projets_beton' AND column_name = 'date_creation'
    ) THEN
        -- Ajouter la colonne date_creation avec valeur par défaut
        ALTER TABLE projets_beton ADD COLUMN date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        -- Mettre à jour les lignes existantes avec la date actuelle
        UPDATE projets_beton SET date_creation = CURRENT_TIMESTAMP WHERE date_creation IS NULL;
        RAISE NOTICE 'Colonne date_creation ajoutée';
    ELSE
        RAISE NOTICE 'Colonne date_creation existe déjà';
    END IF;
END $$;

-- Vérifier les colonnes
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'projets_beton'
ORDER BY ordinal_position;

