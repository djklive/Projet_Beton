-- Script SQL pour créer la table des projets de génie civil
-- À exécuter dans pgAdmin : Tools > Query Tool

-- Créer la base de données si elle n'existe pas
-- CREATE DATABASE db_genie_civil;

-- Table principale des projets
CREATE TABLE IF NOT EXISTS projets_beton (
    id SERIAL PRIMARY KEY,
    
    -- Informations du projet
    nom_projet VARCHAR(200) NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    type_structure VARCHAR(50) NOT NULL, -- (Bâtiment, Pont, Route, Barrage, etc.)
    
    -- Variables de conception
    forme_structure VARCHAR(50), -- (Rectangulaire, Circulaire, Trapézoïdale, etc.)
    longueur_m NUMERIC(10, 2), -- en mètres
    largeur_m NUMERIC(10, 2), -- en mètres
    hauteur_m NUMERIC(10, 2), -- en mètres
    epaisseur_m NUMERIC(10, 3), -- épaisseur du béton en mètres
    
    -- Variables de charge
    charge_statique_kn NUMERIC(10, 2), -- Charge statique en kN
    charge_dynamique_kn NUMERIC(10, 2), -- Charge dynamique en kN
    charge_vent_kn NUMERIC(10, 2), -- Charge du vent en kN
    charge_neige_kn NUMERIC(10, 2), -- Charge de neige en kN
    charge_seisme_kn NUMERIC(10, 2), -- Charge sismique en kN
    
    -- Variables de matériau
    type_beton VARCHAR(50), -- (Ordinaire, Haute résistance, Ultra-haute résistance, etc.)
    resistance_mpa NUMERIC(6, 2), -- Résistance compressive en MPa
    dosage_ciment_kg_m3 NUMERIC(6, 2), -- Dosage de ciment en kg/m³
    dosage_eau_kg_m3 NUMERIC(6, 2), -- Dosage d'eau en kg/m³
    dosage_sable_kg_m3 NUMERIC(6, 2), -- Dosage de sable en kg/m³
    dosage_gravier_kg_m3 NUMERIC(6, 2), -- Dosage de gravier en kg/m³
    
    -- Variables de calcul
    coefficient_securite NUMERIC(4, 2) DEFAULT 1.5, -- Coefficient de sécurité
    
    -- Calculs automatiques
    volume_beton_m3 NUMERIC(10, 3), -- Volume de béton nécessaire en m³
    quantite_ciment_kg NUMERIC(10, 2), -- Quantité totale de ciment en kg
    quantite_eau_kg NUMERIC(10, 2), -- Quantité totale d'eau en kg
    quantite_sable_kg NUMERIC(10, 2), -- Quantité totale de sable en kg
    quantite_gravier_kg NUMERIC(10, 2), -- Quantité totale de gravier en kg
    
    -- Coûts
    cout_ciment_eur NUMERIC(10, 2), -- Coût du ciment en euros
    cout_sable_eur NUMERIC(10, 2), -- Coût du sable en euros
    cout_gravier_eur NUMERIC(10, 2), -- Coût du gravier en euros
    cout_main_oeuvre_eur NUMERIC(10, 2), -- Coût de main-d'œuvre en euros
    cout_total_eur NUMERIC(10, 2), -- Coût total du projet en euros
    
    -- Propriétés calculées
    charge_totale_kn NUMERIC(10, 2), -- Charge totale (statique + dynamique + environnementale)
    contrainte_mpa NUMERIC(6, 2), -- Contrainte appliquée en MPa
    marge_securite NUMERIC(6, 2), -- Marge de sécurité (résistance / contrainte)
    
    -- Dimensions des éléments structurels
    largeur_poutre_m NUMERIC(6, 2), -- Largeur des poutres en mètres
    hauteur_poutre_m NUMERIC(6, 2), -- Hauteur des poutres en mètres
    largeur_colonne_m NUMERIC(6, 2), -- Largeur des colonnes en mètres
    epaisseur_dalle_m NUMERIC(6, 2), -- Épaisseur des dalles en mètres
    
    -- Résistance et déformation
    resistance_structure_mpa NUMERIC(6, 2), -- Résistance structurelle calculée en MPa
    deformation NUMERIC(10, 6), -- Déformation de la structure
    deplacement_mm NUMERIC(10, 2), -- Déplacement estimé en millimètres
    
    -- Planification
    duree_projet_jours INTEGER, -- Durée estimée du projet en jours
    cout_materiaux_eur NUMERIC(10, 2), -- Coût total des matériaux en euros
    
    -- Notes et observations
    notes TEXT,
    statut VARCHAR(50) DEFAULT 'En conception' -- (En conception, Approuvé, En construction, Terminé)
);

-- Commentaires sur les colonnes
COMMENT ON TABLE projets_beton IS 'Table de stockage des projets de génie civil en béton';
COMMENT ON COLUMN projets_beton.volume_beton_m3 IS 'Volume de béton calculé automatiquement';
COMMENT ON COLUMN projets_beton.marge_securite IS 'Marge de sécurité = Résistance / Contrainte (doit être > coefficient_securite)';

-- Vérification de la structure
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'projets_beton'
ORDER BY ordinal_position;

-- Message de confirmation
SELECT 'Table projets_beton créée avec succès !' AS message;

