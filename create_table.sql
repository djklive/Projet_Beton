-- Script SQL pour créer la table dossiers_patients
-- À exécuter dans pgAdmin : Tools > Query Tool > Coller ce code > Execute

-- Supprimer la table si elle existe déjà (ATTENTION : perte de données)
-- DROP TABLE IF EXISTS dossiers_patients;

-- Créer la table
CREATE TABLE IF NOT EXISTS dossiers_patients (
    -- Identifiant auto-incrémenté
    id                      SERIAL PRIMARY KEY,
    
    -- Identité du patient
    patient_ref_id          VARCHAR(100) NOT NULL UNIQUE,
    date_naissance          DATE NOT NULL,
    sexe                    VARCHAR(10) NOT NULL,
    
    -- Données de la visite (collectées par l'infirmière)
    date_visite             TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    poids_kg                NUMERIC(5, 2),
    taille_cm               NUMERIC(5, 1),
    tension_systolique      INTEGER,
    tension_diastolique     INTEGER,
    temperature_celsius     NUMERIC(4, 2),
    
    -- Calculs et annotations (médecin)
    imc                     NUMERIC(5, 2),
    diagnostic_primaire     TEXT,
    notes_medecin           TEXT
);

-- Commentaires sur les colonnes (documentation)
COMMENT ON TABLE dossiers_patients IS 'Table de stockage des données patients collectées et analysées';
COMMENT ON COLUMN dossiers_patients.patient_ref_id IS 'Identifiant unique du patient (ex: PAT-001)';
COMMENT ON COLUMN dossiers_patients.imc IS 'Indice de Masse Corporelle (calculé automatiquement)';
COMMENT ON COLUMN dossiers_patients.date_visite IS 'Date et heure de la visite (automatique si non spécifiée)';

-- Vérification : Afficher la structure de la table
SELECT 
    column_name, 
    data_type, 
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'dossiers_patients'
ORDER BY ordinal_position;

-- Message de confirmation
SELECT 'Table dossiers_patients creee avec succes !' AS message;

-- (Optionnel) Insérer des données de test
-- INSERT INTO dossiers_patients (patient_ref_id, date_naissance, sexe, poids_kg, taille_cm, tension_systolique, tension_diastolique, temperature_celsius, imc)
-- VALUES 
--     ('PAT-001', '1990-01-15', 'Homme', 70.5, 175.0, 120, 80, 37.0, 23.02),
--     ('PAT-002', '1985-05-20', 'Femme', 65.2, 165.0, 115, 75, 36.8, 23.94),
--     ('PAT-003', '1995-09-30', 'Homme', 85.0, 180.0, 135, 90, 37.2, 26.23);

