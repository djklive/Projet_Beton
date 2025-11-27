-- Script SQL simplifié pour créer la table projets_beton
-- À exécuter directement dans Railway PostgreSQL (interface web ou CLI)

-- Supprimer la table si elle existe déjà (optionnel, seulement si vous voulez repartir de zéro)
-- DROP TABLE IF EXISTS projets_beton CASCADE;

CREATE TABLE IF NOT EXISTS projets_beton (
    id SERIAL PRIMARY KEY,
    nom_projet VARCHAR(255) NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    type_structure VARCHAR(100),
    forme_structure VARCHAR(50),
    longueur_m NUMERIC(10, 2),
    largeur_m NUMERIC(10, 2),
    hauteur_m NUMERIC(10, 2),
    epaisseur_m NUMERIC(10, 3),
    charge_statique_kn NUMERIC(10, 2),
    charge_dynamique_kn NUMERIC(10, 2),
    charge_vent_kn NUMERIC(10, 2),
    charge_neige_kn NUMERIC(10, 2),
    charge_seisme_kn NUMERIC(10, 2),
    type_beton VARCHAR(100),
    resistance_mpa NUMERIC(6, 2),
    dosage_ciment_kg_m3 NUMERIC(6, 2),
    dosage_eau_kg_m3 NUMERIC(6, 2),
    dosage_sable_kg_m3 NUMERIC(6, 2),
    dosage_gravier_kg_m3 NUMERIC(6, 2),
    coefficient_securite NUMERIC(4, 2),
    volume_beton_m3 NUMERIC(10, 3),
    quantite_ciment_kg NUMERIC(10, 2),
    quantite_eau_kg NUMERIC(10, 2),
    quantite_sable_kg NUMERIC(10, 2),
    quantite_gravier_kg NUMERIC(10, 2),
    cout_ciment_eur NUMERIC(10, 2),
    cout_sable_eur NUMERIC(10, 2),
    cout_gravier_eur NUMERIC(10, 2),
    cout_main_oeuvre_eur NUMERIC(10, 2),
    cout_total_eur NUMERIC(10, 2),
    charge_totale_kn NUMERIC(10, 2),
    contrainte_mpa NUMERIC(6, 2),
    marge_securite NUMERIC(6, 2),
    largeur_poutre_m NUMERIC(6, 2),
    hauteur_poutre_m NUMERIC(6, 2),
    largeur_colonne_m NUMERIC(6, 2),
    epaisseur_dalle_m NUMERIC(6, 2),
    resistance_structure_mpa NUMERIC(6, 2),
    deformation NUMERIC(10, 6),
    deplacement_mm NUMERIC(10, 2),
    duree_projet_jours INTEGER,
    cout_materiaux_eur NUMERIC(10, 2),
    notes TEXT,
    statut VARCHAR(50)
);

-- Vérifier que la table a été créée
SELECT 
    'Table projets_beton créée avec succès!' as message,
    COUNT(*) as nombre_colonnes
FROM information_schema.columns 
WHERE table_name = 'projets_beton';

