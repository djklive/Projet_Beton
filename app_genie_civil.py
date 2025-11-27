"""
Application de Gestion de Projets Béton
Développée avec Shiny for Python et PostgreSQL

Modules:
    - Module Ingénieur: Saisie et calcul de projets béton
    - Module Analyste: Analyse statistique des projets (résistance, coûts, charges)
"""

from shiny import App, render, ui, reactive
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Configuration de la connexion à PostgreSQL
# Support des variables d'environnement pour Railway et autres plateformes
import os

# Fonction pour obtenir l'URL de la base de données
def get_database_url():
    """Récupère l'URL de connexion PostgreSQL depuis les variables d'environnement"""
    # Railway/Heroku fournissent DATABASE_URL directement
    # Vérifier d'abord DATABASE_URL (priorité)
    db_url = os.getenv("DATABASE_URL")
    
    # Debug: afficher si DATABASE_URL existe (sans afficher la valeur complète pour sécurité)
    if db_url:
        print(f"[CONFIG] DATABASE_URL trouvée (longueur: {len(db_url)} caractères)")
        print(f"[CONFIG] DATABASE_URL commence par: {db_url[:20]}...")
        
        # Railway/Heroku fournissent DATABASE_URL au format: postgresql://user:pass@host:port/db
        # Adapter si nécessaire pour psycopg2
        if db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
            print(f"[CONFIG] URL adaptée pour psycopg2")
        
        print(f"[CONFIG] ✅ Utilisation de DATABASE_URL depuis variables d'environnement Railway")
        return db_url
    else:
        # Configuration locale (développement) via variables individuelles
        print(f"[CONFIG] ⚠️ DATABASE_URL non trouvée, utilisation de la configuration locale")
        POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
        POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Djoko002&")
        POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
        POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
        POSTGRES_DB = os.getenv("POSTGRES_DB", "db_genie_civil")
        
        # Encoder le mot de passe pour gérer les caractères spéciaux comme &
        encoded_password = quote_plus(POSTGRES_PASSWORD)
        db_url = f"postgresql+psycopg2://{POSTGRES_USER}:{encoded_password}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        print(f"[CONFIG] Configuration locale (host: {POSTGRES_HOST}, db: {POSTGRES_DB})")
        return db_url

# Créer l'engine avec lazy initialization (ne se connecte pas immédiatement)
DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

# Fonction pour tester la connexion (appelée de manière non-bloquante)
def test_connection():
    """Teste la connexion PostgreSQL de manière non-bloquante"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"[DB] Connexion PostgreSQL réussie! Version: {version[:50]}...")
            
            # Vérifier que la table existe
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'projets_beton'
                );
            """))
            table_exists = result.fetchone()[0]
            if table_exists:
                print("[DB] Table 'projets_beton' existe")
            else:
                print("[DB] ⚠️ Table 'projets_beton' N'EXISTE PAS - Veuillez exécuter create_table_genie_civil.sql")
            return True
    except Exception as e:
        print(f"[DB] ⚠️ Erreur de connexion (non bloquant): {str(e)[:100]}")
        print("[DB] La connexion sera réessayée lors de la première utilisation")
        return False

# Fonction pour initialiser la table si elle n'existe pas
def init_database_table():
    """Crée la table projets_beton si elle n'existe pas"""
    try:
        with engine.connect() as conn:
            # Vérifier si la table existe
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'projets_beton'
                );
            """))
            table_exists = result.fetchone()[0]
            
            if not table_exists:
                print("[DB] Table 'projets_beton' n'existe pas. Création en cours...")
                # Lire et exécuter le script SQL
                try:
                    with open("create_table_genie_civil.sql", "r", encoding="utf-8") as f:
                        sql_script = f.read()
                    conn.execute(text(sql_script))
                    conn.commit()
                    print("[DB] ✅ Table 'projets_beton' créée avec succès!")
                except FileNotFoundError:
                    print("[DB] ⚠️ Fichier create_table_genie_civil.sql introuvable")
                    print("[DB] Création de la table avec le script intégré...")
                    # Script SQL intégré comme fallback
                    create_table_sql = """
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
                    """
                    conn.execute(text(create_table_sql))
                    conn.commit()
                    print("[DB] ✅ Table créée avec le script intégré!")
            else:
                print("[DB] Table 'projets_beton' existe déjà")
    except Exception as e:
        print(f"[DB] ⚠️ Erreur lors de l'initialisation de la table: {str(e)[:200]}")
        print("[DB] L'application continuera, mais certaines fonctionnalités peuvent ne pas fonctionner")

# Tester la connexion et initialiser la table en arrière-plan (non bloquant)
print("[INIT] Initialisation de l'application...")
print(f"[INIT] DATABASE_URL finale configurée: {'Oui' if DATABASE_URL else 'Non'}")
if DATABASE_URL:
    # Afficher un aperçu de l'URL (sans les credentials)
    url_parts = DATABASE_URL.split("@")
    if len(url_parts) > 1:
        print(f"[INIT] Connexion à: ...@{url_parts[1]}")
    else:
        print(f"[INIT] Format URL: {DATABASE_URL[:30]}...")

if test_connection():
    init_database_table()
else:
    print("[INIT] ⚠️ Connexion échouée au démarrage, mais l'application continuera")
    print("[INIT] La connexion sera réessayée lors de la première utilisation")

# Configuration du style des graphiques
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_theme(style="whitegrid", palette="Blues")

# Style CSS personnalisé pour l'application
CUSTOM_CSS = """
<style>
:root {
    --primary-blue: #0066cc;
    --secondary-blue: #4a90e2;
    --light-blue: #e8f4f8;
    --dark-blue: #004080;
    --white: #ffffff;
    --light-gray: #f5f5f5;
    --medium-gray: #cccccc;
    --dark-gray: #666666;
    --text-dark: #333333;
}

/* Navbar responsive */
.navbar {
    background-color: var(--primary-blue) !important;
    border-bottom: 2px solid var(--dark-blue);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar-nav {
    flex-wrap: wrap;
}

.nav-link {
    color: var(--white) !important;
    font-weight: 500;
    padding: 0.75rem 1rem !important;
    transition: background-color 0.3s ease;
    border-radius: 4px;
    margin: 0.25rem;
}

.nav-link:hover {
    background-color: var(--secondary-blue) !important;
    color: var(--white) !important;
}

.nav-link.active {
    background-color: var(--dark-blue) !important;
    color: var(--white) !important;
}

/* Responsive navbar */
@media (max-width: 768px) {
    .navbar-nav {
        flex-direction: column;
        width: 100%;
    }
    
    .nav-link {
        width: 100%;
        text-align: left;
        padding: 0.75rem 1rem !important;
    }
}

/* Container principal */
.main-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem 1rem;
    background-color: var(--white);
}

/* Titres */
h1, h2, h3, h4, h5, h6 {
    color: var(--primary-blue);
    font-weight: 600;
}

h2 {
    border-bottom: 2px solid var(--light-blue);
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem;
}

/* Sections */
.section {
    background-color: var(--white);
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border: 2px solid var(--light-blue);
}

.section-header {
    color: var(--primary-blue);
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--light-blue);
}

/* Formulaires */
.form-control, .form-select, input[type="text"], input[type="number"], select {
    border: 2px solid var(--medium-gray) !important;
    border-radius: 6px !important;
    padding: 0.75rem !important;
    transition: all 0.3s ease !important;
    background-color: var(--white) !important;
    font-size: 1rem !important;
    width: 100% !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
}

.form-control:focus, .form-select:focus, input[type="text"]:focus, input[type="number"]:focus, select:focus {
    border-color: var(--primary-blue) !important;
    box-shadow: 0 0 0 0.3rem rgba(0, 102, 204, 0.25) !important;
    outline: none !important;
}

.form-control:hover, .form-select:hover, input[type="text"]:hover, input[type="number"]:hover, select:hover {
    border-color: var(--secondary-blue) !important;
}

/* Labels */
label {
    font-weight: 600 !important;
    color: var(--primary-blue) !important;
    margin-bottom: 0.5rem !important;
    display: block !important;
}

/* Boutons */
.btn-primary {
    background-color: var(--primary-blue);
    border-color: var(--primary-blue);
    color: var(--white);
    font-weight: 500;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    background-color: var(--dark-blue);
    border-color: var(--dark-blue);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

/* Cards */
.card {
    background-color: var(--white);
    border: 1px solid var(--medium-gray);
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.card-header {
    background-color: var(--light-blue);
    color: var(--primary-blue);
    font-weight: 600;
    padding: 1rem;
    border-bottom: 2px solid var(--primary-blue);
    border-radius: 8px 8px 0 0;
}

/* Tables */
table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin: 1.5rem 0 !important;
    border: 2px solid var(--primary-blue) !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    background-color: var(--white) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}

table th {
    background-color: var(--primary-blue) !important;
    color: var(--white) !important;
    padding: 1rem 0.75rem !important;
    text-align: left !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: 1px solid var(--dark-blue) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

table td {
    padding: 1rem 0.75rem !important;
    border: 1px solid var(--medium-gray) !important;
    background-color: var(--white) !important;
    font-size: 0.95rem !important;
}

table tr:nth-child(even) td {
    background-color: var(--light-gray) !important;
}

table tr:hover td {
    background-color: var(--light-blue) !important;
    transition: background-color 0.2s ease !important;
}

table tbody tr:last-child td {
    border-bottom: none !important;
}

/* Sidebar */
.sidebar {
    background-color: var(--light-gray);
    border-right: 1px solid var(--medium-gray);
    padding: 1.5rem;
}

/* Responsive */
@media (max-width: 992px) {
    .main-container {
        padding: 1rem 0.5rem;
    }
    
    .section {
        padding: 1rem;
    }
}

@media (max-width: 768px) {
    h2 {
        font-size: 1.5rem;
    }
    
    .section-header {
        font-size: 1.1rem;
    }
    
    .btn-primary {
        width: 100%;
        margin-bottom: 0.5rem;
    }
}

/* Alertes et messages */
.alert {
    padding: 1rem;
    border-radius: 4px;
    margin-bottom: 1rem;
}

.alert-success {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
}

.alert-danger {
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
}

.alert-warning {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    color: #856404;
}

.alert-info {
    background-color: var(--light-blue);
    border: 1px solid var(--secondary-blue);
    color: var(--dark-blue);
}

/* Badges */
.badge {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.875rem;
    font-weight: 600;
}

.badge-primary {
    background-color: var(--primary-blue);
    color: var(--white);
}

.badge-success {
    background-color: #28a745;
    color: var(--white);
}

.badge-danger {
    background-color: #dc3545;
    color: var(--white);
}

/* Layout responsive */
@media (max-width: 576px) {
    .layout-columns {
        flex-direction: column;
    }
    
    .col-3, .col-4, .col-6 {
        width: 100% !important;
        margin-bottom: 1rem;
    }
}

/* Styles spécifiques pour Shiny inputs */
.shiny-input-container input[type="text"],
.shiny-input-container input[type="number"],
.shiny-input-container select {
    border: 2px solid var(--medium-gray) !important;
    border-radius: 6px !important;
    padding: 0.75rem !important;
    transition: all 0.3s ease !important;
    background-color: var(--white) !important;
    font-size: 1rem !important;
    width: 100% !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    display: block !important;
}

.shiny-input-container input[type="text"]:focus,
.shiny-input-container input[type="number"]:focus,
.shiny-input-container select:focus {
    border-color: var(--primary-blue) !important;
    box-shadow: 0 0 0 0.3rem rgba(0, 102, 204, 0.25) !important;
    outline: none !important;
}

.shiny-input-container input[type="text"]:hover,
.shiny-input-container input[type="number"]:hover,
.shiny-input-container select:hover {
    border-color: var(--secondary-blue) !important;
}

.shiny-input-container label {
    font-weight: 600 !important;
    color: var(--primary-blue) !important;
    margin-bottom: 0.5rem !important;
    display: block !important;
    font-size: 1rem !important;
}

/* Amélioration des tableaux */
table {
    border: 2px solid var(--primary-blue) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
}

table th {
    background: linear-gradient(135deg, var(--primary-blue) 0%, var(--dark-blue) 100%) !important;
    color: var(--white) !important;
    padding: 1rem 0.75rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    font-size: 0.9rem !important;
    border: none !important;
}

table td {
    padding: 1rem 0.75rem !important;
    border: 1px solid var(--medium-gray) !important;
    background-color: var(--white) !important;
}

table tbody tr:nth-child(even) td {
    background-color: #f8f9fa !important;
}

table tbody tr:hover td {
    background-color: var(--light-blue) !important;
    transition: background-color 0.2s ease !important;
}
</style>
"""

# Prix unitaires des matériaux (en euros)
PRIX_CIMENT = 0.15  # €/kg
PRIX_SABLE = 0.05   # €/kg
PRIX_GRAVIER = 0.04 # €/kg
PRIX_MAIN_OEUVRE = 80  # €/m³

# Constantes pour les calculs structurels
MODULE_ELASTICITE_BETON = 30000  # MPa (module d'élasticité du béton)
POISSON_BETON = 0.2  # Coefficient de Poisson
RENDEMENT_MAIN_OEUVRE = 2.5  # m³/jour par ouvrier (productivité)

# ============================================================================
# INTERFACE UTILISATEUR (UI) - Module Ingénieur
# ============================================================================

ui_ingenieur = ui.nav_panel(
    "Saisie Projet", # Titre de la page
    ui.tags.head(ui.tags.style(CUSTOM_CSS)),
    ui.tags.div(
        ui.tags.h2("Module de Conception de Projet Béton"),
        ui.tags.p("Remplissez les informations ci-dessous pour créer un nouveau projet et calculer les quantités de béton nécessaires.", style="color: #666;"),
        ui.tags.br(),
        
        # Section Informations du Projet
        ui.tags.div(
            ui.tags.h4("Informations du Projet", class_="section-header"),
            ui.input_text("nom_projet", "Nom du Projet", "Projet-001", width="100%"),
            ui.input_select(
                "type_structure",
                "Type de Structure",
                {
                    "Bâtiment": "Bâtiment",
                    "Pont": "Pont",
                    "Route": "Route",
                    "Barrage": "Barrage",
                    "Fondation": "Fondation",
                    "Mur de soutènement": "Mur de soutènement",
                    "Autre": "Autre"
                },
                selected="Bâtiment"
            ),
            ui.input_select(
                "forme_structure",
                "Forme de la Structure",
                {
                    "Rectangulaire": "Rectangulaire",
                    "Circulaire": "Circulaire",
                    "Trapézoïdale": "Trapézoïdale",
                    "Irregulière": "Irregulière"
                },
                selected="Rectangulaire"
            ),
            class_="section"
        ),
        
        ui.tags.hr(),
        
        # Section Dimensions
        ui.tags.div(
            ui.tags.h4("Dimensions (en mètres)", class_="section-header"),
            ui.layout_columns(
                ui.input_numeric("longueur_m", "Longueur (m)", value=10.0, min=0.1, max=1000, step=0.1),
                ui.input_numeric("largeur_m", "Largeur (m)", value=5.0, min=0.1, max=1000, step=0.1),
                ui.input_numeric("hauteur_m", "Hauteur (m)", value=3.0, min=0.1, max=500, step=0.1),
                ui.input_numeric("epaisseur_m", "Épaisseur Béton (m)", value=0.2, min=0.05, max=5, step=0.01),
                col_widths=[3, 3, 3, 3]
            ),
            class_="section"
        ),
        
        ui.tags.hr(),
        
        # Section Charges
        ui.tags.div(
            ui.tags.h4("Charges (en kN)", class_="section-header"),
            ui.layout_columns(
                ui.input_numeric("charge_statique_kn", "Charge Statique", value=100.0, min=0, max=100000, step=1),
                ui.input_numeric("charge_dynamique_kn", "Charge Dynamique", value=50.0, min=0, max=100000, step=1),
                ui.input_numeric("charge_vent_kn", "Charge Vent", value=20.0, min=0, max=10000, step=1),
                ui.input_numeric("charge_neige_kn", "Charge Neige", value=10.0, min=0, max=10000, step=1),
                ui.input_numeric("charge_seisme_kn", "Charge Séisme", value=30.0, min=0, max=10000, step=1),
                col_widths=[2, 2, 2, 2, 2]
            ),
            class_="section"
        ),
        
        ui.tags.hr(),
        
        # Section Matériaux
        ui.tags.div(
            ui.tags.h4("Propriétés du Béton", class_="section-header"),
            ui.input_select(
                "type_beton",
                "Type de Béton",
                {
                    "Ordinaire": "Ordinaire",
                    "Haute résistance": "Haute résistance",
                    "Ultra-haute résistance": "Ultra-haute résistance",
                    "Béton léger": "Béton léger",
                    "Béton armé": "Béton armé",
                    "Béton précontraint": "Béton précontraint"
                },
                selected="Ordinaire"
            ),
            ui.input_numeric("resistance_mpa", "Résistance Compressive (MPa)", value=25.0, min=10, max=150, step=1),
            ui.input_numeric("coefficient_securite", "Coefficient de Sécurité", value=1.5, min=1.0, max=3.0, step=0.1),
            ui.tags.h5("Composition du Béton (dosages en kg/m³)", style="color: #0066cc; font-weight: 600; margin-top: 1rem;"),
            ui.layout_columns(
                ui.input_numeric("dosage_ciment_kg_m3", "Ciment (kg/m³)", value=350.0, min=200, max=600, step=10),
                ui.input_numeric("dosage_eau_kg_m3", "Eau (kg/m³)", value=175.0, min=100, max=300, step=5),
                ui.input_numeric("dosage_sable_kg_m3", "Sable (kg/m³)", value=700.0, min=400, max=1200, step=50),
                ui.input_numeric("dosage_gravier_kg_m3", "Gravier (kg/m³)", value=1200.0, min=800, max=1800, step=50),
                col_widths=[3, 3, 3, 3]
            ),
            class_="section"
        ),
        
        ui.tags.hr(),
        
        # Bouton de soumission
        ui.tags.div(
            ui.input_action_button("submit_btn", "Calculer et Enregistrer le Projet", class_="btn-primary btn-lg"),
            style="text-align: center; margin: 2rem 0;"
        ),
        
        ui.tags.br(),
        
        # Zone de résultats
        ui.tags.div(
            ui.output_text_verbatim("submit_message_output"),
            ui.output_ui("calculs_output"),
            class_="section"
        ),
        class_="main-container"
    )
)

# ============================================================================
# INTERFACE UTILISATEUR (UI) - Module Analyste
# ============================================================================

ui_consultation = ui.nav_panel(
    "Consultation Projets",
    ui.tags.head(ui.tags.style(CUSTOM_CSS)),
    ui.tags.div(
        ui.tags.h2("Consultation des Résultats par Projet"),
        ui.tags.p("Sélectionnez un projet pour voir tous ses résultats détaillés.", style="color: #666;"),
        
        ui.layout_sidebar(
            ui.sidebar(
                ui.tags.h5("Selection du Projet", style="color: #0066cc; font-weight: 600;"),
                ui.output_ui("liste_projets_ui"),
                ui.tags.hr(),
                ui.output_ui("info_projet_selectionne"),
                width=300
            ),
            
            ui.output_ui("resultats_projet_detail")
        ),
        class_="main-container"
    )
)

ui_analyste = ui.nav_panel(
    "Tableau de Bord Analyste",
    ui.tags.head(ui.tags.style(CUSTOM_CSS)),
    ui.tags.div(
        ui.tags.h2("Analyse Statistique des Projets Béton"),
        ui.tags.p("Sélectionnez les variables à analyser pour comprendre les relations entre les paramètres de conception.", style="color: #666;"),
        
        ui.layout_sidebar(
            ui.sidebar(
                # Section Analyse Univariée
                ui.tags.h5("Analyse Univariée", style="color: #0066cc; font-weight: 600;"),
                ui.input_select(
                    "var_univar",
                    "Variable (Distribution)",
                    {
                        "volume_beton_m3": "Volume Béton (m³)",
                        "resistance_mpa": "Résistance (MPa)",
                        "charge_totale_kn": "Charge Totale (kN)",
                        "cout_total_eur": "Coût Total (€)",
                        "marge_securite": "Marge de Sécurité",
                        "longueur_m": "Longueur (m)",
                        "epaisseur_m": "Épaisseur (m)"
                    },
                    selected="volume_beton_m3"
                ),
                
                ui.tags.hr(),
                
                # Section Analyse Bivariée
                ui.tags.h5("Analyse Bivariée (Corrélation)", style="color: #0066cc; font-weight: 600;"),
                ui.input_select(
                    "var_bivar1",
                    "Variable X",
                    {
                        "volume_beton_m3": "Volume Béton",
                        "resistance_mpa": "Résistance",
                        "charge_totale_kn": "Charge Totale",
                        "cout_total_eur": "Coût Total",
                        "longueur_m": "Longueur",
                        "epaisseur_m": "Épaisseur"
                    },
                    selected="volume_beton_m3"
                ),
                ui.input_select(
                    "var_bivar2",
                    "Variable Y",
                    {
                        "cout_total_eur": "Coût Total",
                        "resistance_mpa": "Résistance",
                        "charge_totale_kn": "Charge Totale",
                        "marge_securite": "Marge Sécurité",
                        "largeur_m": "Largeur",
                        "hauteur_m": "Hauteur"
                    },
                    selected="cout_total_eur"
                ),
                
                ui.tags.hr(),
                
                # Filtres
                ui.tags.h5("Filtres", style="color: #0066cc; font-weight: 600;"),
                ui.input_select(
                    "filtre_type",
                    "Type de Structure",
                    {
                        "Tous": "Tous",
                        "Bâtiment": "Bâtiment",
                        "Pont": "Pont",
                        "Route": "Route",
                        "Barrage": "Barrage"
                    },
                    selected="Tous"
                ),
                
                ui.tags.hr(),
                
                # Statistiques globales
                ui.output_ui("stats_summary"),
                
                width=300
            ),
            
            # Graphique Univarié
            ui.tags.h4("Distribution Univariée", class_="section-header"),
            ui.output_plot("plot_univar", height="400px"),
            
            ui.tags.br(), ui.tags.br(),
            
            # Graphique Bivarié
            ui.tags.h4("Analyse de Corrélation (Bivariée)", class_="section-header"),
            ui.output_plot("plot_bivar", height="400px"),
            
            ui.tags.br(), ui.tags.br(),
            
            # Résultats des tests statistiques
            ui.tags.h4("Tests de Corrélation", class_="section-header"),
            ui.output_text_verbatim("correlation_output"),
        ),
        class_="main-container"
    )
)

# ============================================================================
# UI PRINCIPALE - Application avec Navigation par Onglets
# ============================================================================

app_ui = ui.page_navbar(
    ui_ingenieur,
    ui_consultation,
    ui_analyste,
    title="Application de Gestion des Projets Béton",
    bg="#0066cc",
    inverse=True,
    sidebar=None
)

# ============================================================================
# LOGIQUE SERVEUR (SERVER)
# ============================================================================

def server(input, output, session):
    """Fonction serveur contenant toute la logique de l'application"""
    
    # Variables réactives pour stocker les messages
    submit_message = reactive.Value("")
    calculs_html = reactive.Value(ui.tags.p(""))
    
    # ------------------------------------------------------------------------
    # PARTIE I: MODULE INGÉNIEUR - Calculs et Enregistrement
    # ------------------------------------------------------------------------
    
    @reactive.Effect
    @reactive.event(input.submit_btn)
    def handle_submission():
        """Gère le calcul et l'enregistrement du projet béton"""
        print("BOUTON CLIQUE - Début des calculs...")
        try:
            # ================================================================
            # CALCULS AUTOMATIQUES
            # ================================================================
            
            # 1. Calcul du volume de béton selon la forme
            longueur = input.longueur_m()
            largeur = input.largeur_m()
            hauteur = input.hauteur_m()
            epaisseur = input.epaisseur_m()
            
            if input.forme_structure() == "Rectangulaire":
                volume_beton = longueur * largeur * epaisseur
            elif input.forme_structure() == "Circulaire":
                # Pour une structure circulaire, on utilise le diamètre comme longueur
                rayon = longueur / 2
                volume_beton = np.pi * (rayon ** 2) * epaisseur
            elif input.forme_structure() == "Trapézoïdale":
                # Approximation : moyenne des bases
                volume_beton = ((longueur + largeur) / 2) * largeur * epaisseur
            else:  # Irrégulière
                volume_beton = longueur * largeur * epaisseur * 0.8  # Facteur de correction
            
            # 2. Calcul des quantités de matériaux
            quantite_ciment = volume_beton * input.dosage_ciment_kg_m3()
            quantite_eau = volume_beton * input.dosage_eau_kg_m3()
            quantite_sable = volume_beton * input.dosage_sable_kg_m3()
            quantite_gravier = volume_beton * input.dosage_gravier_kg_m3()
            
            # 3. Calcul des charges totales
            charge_totale = (
                input.charge_statique_kn() +
                input.charge_dynamique_kn() +
                input.charge_vent_kn() +
                input.charge_neige_kn() +
                input.charge_seisme_kn()
            )
            
            # 4. Calcul de la contrainte appliquée (simplifié)
            # Contrainte = Charge / Surface
            surface_m2 = longueur * largeur
            if surface_m2 > 0:
                contrainte_mpa = (charge_totale * 1000) / (surface_m2 * 1000000)  # Conversion en MPa
            else:
                contrainte_mpa = 0
            
            # 5. Calcul de la marge de sécurité
            resistance = input.resistance_mpa()
            if contrainte_mpa > 0:
                marge_securite = resistance / contrainte_mpa
            else:
                marge_securite = 999  # Pas de contrainte = sécurité infinie
            
            # 6. Calcul des coûts
            cout_ciment = quantite_ciment * PRIX_CIMENT
            cout_sable = quantite_sable * PRIX_SABLE
            cout_gravier = quantite_gravier * PRIX_GRAVIER
            cout_main_oeuvre = volume_beton * PRIX_MAIN_OEUVRE
            cout_materiaux = cout_ciment + cout_sable + cout_gravier
            cout_total = cout_materiaux + cout_main_oeuvre
            
            # 7. Calcul de la durée du projet (en jours)
            # Basé sur le volume de béton et la productivité
            duree_projet_jours = max(1, int(np.ceil(volume_beton / RENDEMENT_MAIN_OEUVRE)))
            
            # 8. Calcul des dimensions structurelles (poutres, colonnes, dalles)
            # Dimensions simplifiées basées sur les dimensions globales
            if input.type_structure() in ["Bâtiment", "Fondation"]:
                # Pour un bâtiment, on estime les dimensions des éléments
                largeur_poutre = max(0.2, epaisseur * 1.5)  # Largeur de poutre
                hauteur_poutre = max(0.3, epaisseur * 2)    # Hauteur de poutre
                largeur_colonne = max(0.3, epaisseur * 1.5) # Colonnes carrées
                epaisseur_dalle = epaisseur                 # Épaisseur de dalle
            else:
                # Pour ponts, barrages, etc.
                largeur_poutre = max(0.3, epaisseur * 2)
                hauteur_poutre = max(0.5, epaisseur * 3)
                largeur_colonne = max(0.4, epaisseur * 2)
                epaisseur_dalle = epaisseur
            
            # 9. Calcul de la résistance structurelle globale
            # Résistance = Résistance du béton × Facteur de forme × Facteur de sécurité
            facteur_forme = 0.85 if input.forme_structure() == "Rectangulaire" else 0.75
            resistance_structure = resistance * facteur_forme * (1 / input.coefficient_securite())
            
            # 10. Calcul des déplacements et déformations (simplifié)
            # Déformation = Contrainte / Module d'élasticité
            if contrainte_mpa > 0:
                deformation = contrainte_mpa / MODULE_ELASTICITE_BETON
                # Déplacement estimé (simplifié) = déformation × longueur caractéristique
                longueur_caracteristique = max(longueur, largeur, hauteur)
                deplacement_mm = deformation * longueur_caracteristique * 1000  # en mm
            else:
                deformation = 0
                deplacement_mm = 0
            
            print(f"Calculs effectués - Volume: {volume_beton:.2f} m³, Coût: {cout_total:.2f} €, Durée: {duree_projet_jours} jours")
            
            # ================================================================
            # PRÉPARATION DES DONNÉES
            # ================================================================
            
            new_data = {
                "nom_projet": input.nom_projet(),
                "type_structure": input.type_structure(),
                "forme_structure": input.forme_structure(),
                "longueur_m": longueur,
                "largeur_m": largeur,
                "hauteur_m": hauteur,
                "epaisseur_m": epaisseur,
                "charge_statique_kn": input.charge_statique_kn(),
                "charge_dynamique_kn": input.charge_dynamique_kn(),
                "charge_vent_kn": input.charge_vent_kn(),
                "charge_neige_kn": input.charge_neige_kn(),
                "charge_seisme_kn": input.charge_seisme_kn(),
                "type_beton": input.type_beton(),
                "resistance_mpa": resistance,
                "dosage_ciment_kg_m3": input.dosage_ciment_kg_m3(),
                "dosage_eau_kg_m3": input.dosage_eau_kg_m3(),
                "dosage_sable_kg_m3": input.dosage_sable_kg_m3(),
                "dosage_gravier_kg_m3": input.dosage_gravier_kg_m3(),
                "coefficient_securite": input.coefficient_securite(),
                "volume_beton_m3": round(volume_beton, 3),
                "quantite_ciment_kg": round(quantite_ciment, 2),
                "quantite_eau_kg": round(quantite_eau, 2),
                "quantite_sable_kg": round(quantite_sable, 2),
                "quantite_gravier_kg": round(quantite_gravier, 2),
                "cout_ciment_eur": round(cout_ciment, 2),
                "cout_sable_eur": round(cout_sable, 2),
                "cout_gravier_eur": round(cout_gravier, 2),
                "cout_main_oeuvre_eur": round(cout_main_oeuvre, 2),
                "cout_total_eur": round(cout_total, 2),
                "charge_totale_kn": round(charge_totale, 2),
                "contrainte_mpa": round(contrainte_mpa, 2),
                "marge_securite": round(marge_securite, 2),
                "statut": "En conception",
                # Nouvelles colonnes pour résultats détaillés
                "duree_projet_jours": duree_projet_jours,
                "largeur_poutre_m": round(largeur_poutre, 2),
                "hauteur_poutre_m": round(hauteur_poutre, 2),
                "largeur_colonne_m": round(largeur_colonne, 2),
                "epaisseur_dalle_m": round(epaisseur_dalle, 2),
                "resistance_structure_mpa": round(resistance_structure, 2),
                "deformation": round(deformation, 6),
                "deplacement_mm": round(deplacement_mm, 2),
                "cout_materiaux_eur": round(cout_materiaux, 2)
            }
            
            print(f"Données préparées: {new_data['nom_projet']}")
            
            # ================================================================
            # ENREGISTREMENT DANS POSTGRESQL
            # ================================================================
            
            df = pd.DataFrame([new_data])
            
            print("Tentative d'écriture dans PostgreSQL...")
            
            with engine.begin() as conn:
                df.to_sql('projets_beton', conn, if_exists='append', index=False)
            
            print("PROJET ENREGISTRÉ AVEC SUCCÈS!")
            
            # ================================================================
            # AFFICHAGE DES RÉSULTATS
            # ================================================================
            
            msg = f"Projet '{input.nom_projet()}' enregistré avec succès !"
            print(f"Message de succès: {msg}")
            ui.notification_show(msg, duration=5, type="success")
            submit_message.set(msg)
            
            # Créer l'affichage détaillé des calculs avec TOUS les résultats
            calculs_content = ui.tags.div(
                ui.tags.h3("RÉSULTATS COMPLETS DES CALCULS", style="color: #0066cc; text-align: center; margin-bottom: 30px;"),
                
                # ============================================================
                # SECTION 1: RÉSULTATS DE CALCUL
                # ============================================================
                ui.tags.div(
                    ui.tags.h4("1. Résultats de Calcul", class_="section-header"),
                    
                    ui.tags.h5("Quantité de Béton", style="color: #0066cc; font-weight: 600; margin-top: 1rem;"),
                    ui.tags.div(
                        ui.tags.p(
                            ui.tags.strong(f"Volume de béton nécessaire: ", style="font-size: 1.1em;"),
                            ui.tags.span(f"{volume_beton:.2f} m³", style="color: #0066cc; font-size: 1.2em; font-weight: bold;")
                        ),
                        style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 15px;"
                    ),
                    
                    ui.tags.h5("Dimensions des Éléments Structurels", style="color: #0066cc; font-weight: 600; margin-top: 1rem;"),
                    ui.tags.table(
                        ui.tags.thead(
                            ui.tags.tr(
                                ui.tags.th("Élément", style="padding: 10px; background-color: #0066cc; color: white;"),
                                ui.tags.th("Dimensions", style="padding: 10px; background-color: #0066cc; color: white;")
                            )
                        ),
                        ui.tags.tbody(
                            ui.tags.tr(
                                ui.tags.td("Poutres", style="padding: 8px; border: 1px solid #ddd;"),
                                ui.tags.td(f"{largeur_poutre:.2f} m × {hauteur_poutre:.2f} m", style="padding: 8px; border: 1px solid #ddd;")
                            ),
                            ui.tags.tr(
                                ui.tags.td("Colonnes", style="padding: 8px; border: 1px solid #ddd;"),
                                ui.tags.td(f"{largeur_colonne:.2f} m × {largeur_colonne:.2f} m (carrées)", style="padding: 8px; border: 1px solid #ddd;")
                            ),
                            ui.tags.tr(
                                ui.tags.td("Dalles", style="padding: 8px; border: 1px solid #ddd;"),
                                ui.tags.td(f"Épaisseur: {epaisseur_dalle:.2f} m", style="padding: 8px; border: 1px solid #ddd;")
                            ),
                            ui.tags.tr(
                                ui.tags.td("Structure globale", style="padding: 8px; border: 1px solid #ddd; font-weight: bold;"),
                                ui.tags.td(f"{longueur:.2f} m × {largeur:.2f} m × {hauteur:.2f} m", style="padding: 8px; border: 1px solid #ddd; font-weight: bold;")
                            )
                        ),
                        style="width: 100%; border-collapse: collapse; margin-bottom: 20px;"
                    ),
                    
                    ui.tags.h5("Résistance de la Structure", style="color: #0066cc; font-weight: 600; margin-top: 1rem;"),
                    ui.tags.div(
                        ui.tags.ul(
                            ui.tags.li(f"Résistance du béton: {resistance:.2f} MPa"),
                            ui.tags.li(f"Résistance structurelle (avec facteurs): {resistance_structure:.2f} MPa"),
                            ui.tags.li(f"Facteur de forme appliqué: {facteur_forme:.2f}")
                        ),
                        style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 15px; border: 1px solid #0066cc;"
                    ),
                    
                    ui.tags.h5("Déplacement et Déformation", style="color: #0066cc; font-weight: 600; margin-top: 1rem;"),
                    ui.tags.div(
                        ui.tags.ul(
                            ui.tags.li(f"Déformation: {deformation:.6f} (sans unité)"),
                            ui.tags.li(f"Déplacement estimé: {deplacement_mm:.2f} mm"),
                            ui.tags.li(f"Module d'élasticité utilisé: {MODULE_ELASTICITE_BETON:.0f} MPa")
                        ),
                        style="background-color: #d1ecf1; padding: 15px; border-radius: 5px; margin-bottom: 20px;"
                    ),
                    
                    style="margin-bottom: 30px;"
                ),
                
                # ============================================================
                # SECTION 2: COÛTS ET PLANIFICATION
                # ============================================================
                ui.tags.div(
                    ui.tags.h4("2. Coûts et Planification", class_="section-header"),
                    
                    ui.tags.h5("Détail des Coûts", style="color: #0066cc; font-weight: 600; margin-top: 1rem;"),
                    ui.tags.div(
                        ui.tags.h6("Coût des Matériaux:", style="color: #0066cc; font-weight: 600;"),
                        ui.tags.ul(
                            ui.tags.li(f"Ciment: {cout_ciment:.2f} €"),
                            ui.tags.li(f"Sable: {cout_sable:.2f} €"),
                            ui.tags.li(f"Gravier: {cout_gravier:.2f} €"),
                            ui.tags.li(ui.tags.strong(f"Total Matériaux: {cout_materiaux:.2f} €", style="color: #0066cc;"))
                        ),
                        style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 15px; border: 1px solid #0066cc;"
                    ),
                    
                    ui.tags.div(
                        ui.tags.h6("Coût de la Main-d'œuvre:", style="color: #0066cc; font-weight: 600;"),
                        ui.tags.ul(
                            ui.tags.li(f"Coût main-d'œuvre: {cout_main_oeuvre:.2f} €"),
                            ui.tags.li(f"Productivité: {RENDEMENT_MAIN_OEUVRE} m³/jour par ouvrier")
                        ),
                        style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 15px; border: 1px solid #0066cc;"
                    ),
                    
                    ui.tags.div(
                        ui.tags.h6("Coût Total du Projet:", style="color: #0066cc; font-size: 1.2em; font-weight: 600;"),
                        ui.tags.p(
                            ui.tags.strong(f"{cout_total:.2f} €", style="font-size: 1.5em; color: #0066cc;"),
                            style="text-align: center; margin: 10px 0;"
                        ),
                        style="background-color: #e8f4f8; padding: 20px; border-radius: 5px; margin-bottom: 15px; border: 2px solid #0066cc;"
                    ),
                    
                    ui.tags.h5("Durée du Projet", style="color: #0066cc; font-weight: 600; margin-top: 1rem;"),
                    ui.tags.div(
                        ui.tags.p(
                            ui.tags.strong("Durée estimée: ", style="font-size: 1.1em;"),
                            ui.tags.span(f"{duree_projet_jours} jour(s)", style="color: #0066cc; font-size: 1.3em; font-weight: bold;")
                        ),
                        ui.tags.p(
                            f"Basé sur un rendement de {RENDEMENT_MAIN_OEUVRE} m³/jour",
                            style="color: #666; font-size: 0.9em; margin-top: 5px;"
                        ),
                        style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 20px;"
                    ),
                    
                    style="margin-bottom: 30px;"
                ),
                
                # ============================================================
                # SECTION 3: ANALYSE DE SÉCURITÉ
                # ============================================================
                ui.tags.div(
                    ui.tags.h4("3. Analyse de Sécurité", class_="section-header"),
                    
                    ui.tags.div(
                        ui.tags.ul(
                            ui.tags.li(f"Charge totale appliquée: {charge_totale:.2f} kN"),
                            ui.tags.li(f"Contrainte appliquée: {contrainte_mpa:.2f} MPa"),
                            ui.tags.li(f"Résistance du béton: {resistance:.2f} MPa"),
                            ui.tags.li(
                                f"Marge de sécurité: {marge_securite:.2f}",
                                style="color: #0066cc; font-weight: bold; font-size: 1.1em;"
                            ),
                            ui.tags.li(f"Coefficient de sécurité requis: {input.coefficient_securite():.2f}")
                        ),
                        style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 15px;"
                    ),
                    
                    ui.tags.div(
                        ui.tags.p(
                            "Marge de sécurité insuffisante ! La structure ne respecte pas le coefficient de sécurité requis." 
                            if marge_securite < input.coefficient_securite() 
                            else "Marge de sécurité acceptable. La structure respecte les critères de sécurité.",
                            style="color: #0066cc; font-weight: bold; padding: 15px; background-color: #e8f4f8; border-radius: 5px; border-left: 4px solid #0066cc;"
                        ),
                        style="margin-bottom: 20px;"
                    ),
                    
                    style="margin-bottom: 30px;"
                ),
                
                # ============================================================
                # SECTION 4: QUANTITÉS DE MATÉRIAUX
                # ============================================================
                ui.tags.div(
                    ui.tags.h4("4. Quantités de Matériaux Nécessaires", class_="section-header"),
                    
                    ui.tags.table(
                        ui.tags.thead(
                            ui.tags.tr(
                                ui.tags.th("Matériau", style="padding: 10px; background-color: #0066cc; color: white;"),
                                ui.tags.th("Quantité", style="padding: 10px; background-color: #0066cc; color: white;"),
                                ui.tags.th("Unité", style="padding: 10px; background-color: #0066cc; color: white;")
                            )
                        ),
                        ui.tags.tbody(
                            ui.tags.tr(
                                ui.tags.td("Ciment", style="padding: 8px; border: 1px solid #ddd;"),
                                ui.tags.td(f"{quantite_ciment:.0f}", style="padding: 8px; border: 1px solid #ddd; text-align: right;"),
                                ui.tags.td("kg", style="padding: 8px; border: 1px solid #ddd;")
                            ),
                            ui.tags.tr(
                                ui.tags.td("Eau", style="padding: 8px; border: 1px solid #ddd;"),
                                ui.tags.td(f"{quantite_eau:.0f}", style="padding: 8px; border: 1px solid #ddd; text-align: right;"),
                                ui.tags.td("kg", style="padding: 8px; border: 1px solid #ddd;")
                            ),
                            ui.tags.tr(
                                ui.tags.td("Sable", style="padding: 8px; border: 1px solid #ddd;"),
                                ui.tags.td(f"{quantite_sable:.0f}", style="padding: 8px; border: 1px solid #ddd; text-align: right;"),
                                ui.tags.td("kg", style="padding: 8px; border: 1px solid #ddd;")
                            ),
                            ui.tags.tr(
                                ui.tags.td("Gravier", style="padding: 8px; border: 1px solid #ddd;"),
                                ui.tags.td(f"{quantite_gravier:.0f}", style="padding: 8px; border: 1px solid #ddd; text-align: right;"),
                                ui.tags.td("kg", style="padding: 8px; border: 1px solid #ddd;")
                            )
                        ),
                        style="width: 100%; border-collapse: collapse; margin-bottom: 20px;"
                    ),
                    
                    style="margin-bottom: 20px;"
                ),
                
                # ============================================================
                # RÉSUMÉ VISUEL
                # ============================================================
                ui.tags.div(
                    ui.tags.h4("Résumé Exécutif", style="text-align: center; color: #0066cc; margin-top: 30px;"),
                    ui.tags.div(
                        ui.layout_columns(
                            ui.tags.div(
                                ui.tags.h5("Volume", style="text-align: center; color: #0066cc;"),
                                ui.tags.p(f"{volume_beton:.2f} m³", style="text-align: center; font-size: 1.5em; font-weight: bold; color: #0066cc;"),
                                style="background-color: #e8f4f8; padding: 15px; border-radius: 10px;"
                            ),
                            ui.tags.div(
                                ui.tags.h5("Coût Total", style="text-align: center; color: #0066cc;"),
                                ui.tags.p(f"{cout_total:.0f} €", style="text-align: center; font-size: 1.5em; font-weight: bold; color: #0066cc;"),
                                style="background-color: #e8f4f8; padding: 15px; border-radius: 10px; border: 1px solid #0066cc;"
                            ),
                            ui.tags.div(
                                ui.tags.h5("Durée", style="text-align: center; color: #0066cc;"),
                                ui.tags.p(f"{duree_projet_jours} jour(s)", style="text-align: center; font-size: 1.5em; font-weight: bold; color: #0066cc;"),
                                style="background-color: #e8f4f8; padding: 15px; border-radius: 10px; border: 1px solid #0066cc;"
                            ),
                            ui.tags.div(
                                ui.tags.h5("Sécurité", style="text-align: center; color: #0066cc;"),
                                ui.tags.p(
                                    "Attention" if marge_securite < input.coefficient_securite() else "OK",
                                    style="text-align: center; font-size: 1.5em; font-weight: bold; color: #0066cc;"
                                ),
                                style="background-color: #e8f4f8; padding: 15px; border-radius: 10px; border: 1px solid #0066cc;"
                            ),
                            col_widths=[3, 3, 3, 3]
                        ),
                        style="margin-top: 20px;"
                    ),
                    style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #ddd;"
                ),
                
                style="background-color: #ffffff; padding: 30px; border-radius: 15px; margin-top: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);"
            )
            
            calculs_html.set(calculs_content)
            print(f"Résultats affichés")
            
        except Exception as e:
            error_msg = f"Erreur lors de l'enregistrement : {str(e)}"
            print(f"ERREUR DÉTAILLÉE: {e}")
            print(f"Type d'erreur: {type(e).__name__}")
            import traceback
            print(f"Traceback complet:")
            traceback.print_exc()
            ui.notification_show(error_msg, duration=10, type="error")
            submit_message.set(error_msg)
            calculs_html.set(ui.tags.p(""))
    
    # Fonction pour afficher le message de soumission
    @render.text
    @reactive.event(input.submit_btn)
    def submit_message_output():
        return submit_message()
    
    # Fonction pour afficher les calculs
    @render.ui
    @reactive.event(input.submit_btn)
    def calculs_output():
        return calculs_html()
    
    # ------------------------------------------------------------------------
    # PARTIE II: MODULE CONSULTATION - Consultation par Projet
    # ------------------------------------------------------------------------
    
    # Variable réactive pour le projet sélectionné
    projet_selectionne_id = reactive.Value(None)
    
    @reactive.calc
    def charger_tous_projets():
        """Charge tous les projets depuis PostgreSQL"""
        input.submit_btn()  # Se met à jour quand un nouveau projet est ajouté
        try:
            with engine.connect() as conn:
                # Vérifier d'abord quelles colonnes existent
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'projets_beton'
                    ORDER BY ordinal_position;
                """))
                columns = [row[0] for row in result.fetchall()]
                print(f"📋 Colonnes disponibles: {columns}")
                
                # Construire la requête en fonction des colonnes disponibles
                select_cols = []
                if 'id' in columns:
                    select_cols.append('id')
                else:
                    # Utiliser ROW_NUMBER() si id n'existe pas
                    select_cols.append('ROW_NUMBER() OVER (ORDER BY nom_projet) as id')
                
                select_cols.extend(['nom_projet', 'type_structure'])
                
                if 'date_creation' in columns:
                    select_cols.append('date_creation')
                
                select_cols.extend(['volume_beton_m3', 'cout_total_eur'])
                
                # Construire la clause ORDER BY
                order_by = 'date_creation DESC' if 'date_creation' in columns else 'nom_projet ASC'
                
                query = f"SELECT {', '.join(select_cols)} FROM projets_beton ORDER BY {order_by}"
                print(f"🔍 Requête SQL: {query}")
                
                df = pd.read_sql(text(query), conn)
                return df
        except Exception as e:
            print(f"Erreur de chargement des projets: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    @render.ui
    def liste_projets_ui():
        """Affiche la liste des projets avec sélection"""
        df = charger_tous_projets()
        
        if df.empty:
            return ui.tags.div(
                ui.tags.p("Aucun projet enregistré", style="color: #666; font-weight: 500;"),
                ui.tags.p("Créez un projet dans l'onglet 'Saisie Projet'", style="color: #666; font-size: 0.9em;")
            )
        
        # Créer les options pour le select
        # IMPORTANT: Les clés sont les IDs (entiers ou noms), les valeurs sont les labels (texte)
        options = {}
        for idx, row in df.iterrows():
            # Utiliser l'index si id n'existe pas, sinon utiliser id
            if 'id' in row and pd.notna(row['id']):
                projet_id = int(row['id'])
            else:
                # Utiliser le nom_projet comme identifiant unique
                projet_id = str(row['nom_projet'])
            
            nom = row['nom_projet']
            type_struct = row.get('type_structure', 'N/A')
            volume = row.get('volume_beton_m3', 0) if pd.notna(row.get('volume_beton_m3')) else 0
            cout = row.get('cout_total_eur', 0) if pd.notna(row.get('cout_total_eur')) else 0
            date_crea = row.get('date_creation', None)
            
            # Formater la date
            if pd.notna(date_crea) and date_crea is not None:
                if isinstance(date_crea, pd.Timestamp):
                    date_str = date_crea.strftime('%d/%m/%Y')
                else:
                    date_str = str(date_crea)[:10]
            else:
                date_str = ""
            
            # Créer le label avec ou sans date
            if date_str:
                label = f"{nom} ({type_struct}) - {volume:.1f}m³ - {cout:.0f}€ - {date_str}"
            else:
                label = f"{nom} ({type_struct}) - {volume:.1f}m³ - {cout:.0f}€"
            
            # Clé = ID (entier ou string), Valeur = Label (texte)
            options[projet_id] = label
        
        return ui.tags.div(
            ui.input_select(
                "projet_selectionne",
                "Choisir un projet",
                options,
                selected=None
            ),
            ui.tags.p(f"Total: {len(df)} projet(s)", style="color: #666; font-size: 0.9em; margin-top: 10px;")
        )
    
    @reactive.calc
    def projet_detail():
        """Charge les détails du projet sélectionné"""
        projet_id = input.projet_selectionne()
        if projet_id is None:
            return None
        
        try:
            # S'assurer que projet_id est un entier
            if isinstance(projet_id, str):
                # Si c'est une chaîne, essayer de la convertir
                try:
                    projet_id = int(projet_id)
                except ValueError:
                    print(f"ID de projet invalide: {projet_id}")
                    return None
            
            print(f"Chargement du projet ID: {projet_id} (type: {type(projet_id).__name__})")
            
            with engine.connect() as conn:
                # Vérifier si la colonne id existe
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'projets_beton' AND column_name = 'id';
                """))
                has_id_column = result.fetchone() is not None
                
                if has_id_column:
                    # Utiliser id si disponible
                    df = pd.read_sql(
                        text("SELECT * FROM projets_beton WHERE id = :id"),
                        conn,
                        params={"id": int(projet_id)}
                    )
                else:
                    # Utiliser nom_projet comme identifiant
                    df = pd.read_sql(
                        text("SELECT * FROM projets_beton WHERE nom_projet = :nom"),
                        conn,
                        params={"nom": str(projet_id)}
                    )
                if not df.empty:
                    print(f"Projet chargé: {df.iloc[0].get('nom_projet', 'N/A')}")
                    return df.iloc[0].to_dict()
                else:
                    print(f"Aucun projet trouvé avec l'ID: {projet_id}")
        except Exception as e:
            print(f"Erreur chargement projet: {e}")
            import traceback
            traceback.print_exc()
        return None
    
    @render.ui
    def info_projet_selectionne():
        """Affiche les informations de base du projet sélectionné"""
        projet = projet_detail()
        if projet is None:
            return ui.tags.p("Sélectionnez un projet", style="color: #999;")
        
        return ui.tags.div(
            ui.tags.h6("Informations", style="color: #0066cc; font-weight: 600;"),
            ui.tags.p(ui.tags.strong("Nom: "), projet.get('nom_projet', 'N/A')),
            ui.tags.p(ui.tags.strong("Type: "), projet.get('type_structure', 'N/A')),
            ui.tags.p(ui.tags.strong("Forme: "), projet.get('forme_structure', 'N/A')),
            ui.tags.p(ui.tags.strong("Statut: "), projet.get('statut', 'N/A')),
            style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;"
        )
    
    @render.ui
    def resultats_projet_detail():
        """Affiche tous les résultats détaillés du projet sélectionné"""
        projet = projet_detail()
        
        if projet is None:
            return ui.tags.div(
                ui.tags.h3("Consultation des Résultats", style="text-align: center; color: #999;"),
                ui.tags.p("Sélectionnez un projet dans le menu de gauche pour voir ses résultats détaillés.", 
                         style="text-align: center; color: #666; margin-top: 50px; font-size: 1.1em;")
            )
        
        # Extraire toutes les valeurs (avec gestion des valeurs None)
        def safe_get(key, default=0, format_func=lambda x: x):
            val = projet.get(key, default)
            if pd.isna(val) or val is None:
                return default
            return format_func(val)
        
        # Créer l'affichage complet des résultats
        return ui.tags.div(
            ui.tags.h3(f"Résultats Complets - {projet.get('nom_projet', 'Projet')}", 
                      style="color: #0066cc; text-align: center; margin-bottom: 30px; border-bottom: 3px solid #0066cc; padding-bottom: 15px;"),
            
            # ============================================================
            # SECTION 1: RÉSULTATS DE CALCUL
            # ============================================================
            ui.tags.div(
                ui.tags.h4("1. Résultats de Calcul", class_="section-header"),
                
                ui.tags.h5("Quantité de Béton", style="color: #0066cc; font-weight: 600; margin-top: 1rem;"),
                ui.tags.div(
                    ui.tags.p(
                        ui.tags.strong("Volume de béton nécessaire: ", style="font-size: 1.1em;"),
                        ui.tags.span(f"{safe_get('volume_beton_m3', 0, lambda x: f'{x:.2f}')} m³", 
                                   style="color: #0066cc; font-size: 1.2em; font-weight: bold;")
                    ),
                    style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 15px;"
                ),
                
                ui.tags.h5("Dimensions des Éléments Structurels", style="color: #0066cc; font-weight: 600; margin-top: 1rem;"),
                ui.tags.table(
                    ui.tags.thead(
                        ui.tags.tr(
                            ui.tags.th("Élément", style="padding: 10px; background-color: #0066cc; color: white;"),
                            ui.tags.th("Dimensions", style="padding: 10px; background-color: #0066cc; color: white;")
                        )
                    ),
                    ui.tags.tbody(
                        ui.tags.tr(
                            ui.tags.td("Poutres", style="padding: 8px; border: 1px solid #ddd;"),
                            ui.tags.td(f"{safe_get('largeur_poutre_m', 0, lambda x: f'{x:.2f}')} m × {safe_get('hauteur_poutre_m', 0, lambda x: f'{x:.2f}')} m", 
                                     style="padding: 8px; border: 1px solid #ddd;")
                        ),
                        ui.tags.tr(
                            ui.tags.td("Colonnes", style="padding: 8px; border: 1px solid #ddd;"),
                            ui.tags.td(f"{safe_get('largeur_colonne_m', 0, lambda x: f'{x:.2f}')} m × {safe_get('largeur_colonne_m', 0, lambda x: f'{x:.2f}')} m (carrées)", 
                                     style="padding: 8px; border: 1px solid #ddd;")
                        ),
                        ui.tags.tr(
                            ui.tags.td("Dalles", style="padding: 8px; border: 1px solid #ddd;"),
                            ui.tags.td(f"Épaisseur: {safe_get('epaisseur_dalle_m', 0, lambda x: f'{x:.2f}')} m", 
                                     style="padding: 8px; border: 1px solid #ddd;")
                        ),
                        ui.tags.tr(
                            ui.tags.td("Structure globale", style="padding: 8px; border: 1px solid #ddd; font-weight: bold;"),
                            ui.tags.td(f"{safe_get('longueur_m', 0, lambda x: f'{x:.2f}')} m × {safe_get('largeur_m', 0, lambda x: f'{x:.2f}')} m × {safe_get('hauteur_m', 0, lambda x: f'{x:.2f}')} m", 
                                     style="padding: 8px; border: 1px solid #ddd; font-weight: bold;")
                        )
                    ),
                    style="width: 100%; border-collapse: collapse; margin-bottom: 20px;"
                ),
                
                ui.tags.h5("Résistance de la Structure", style="color: #0066cc; font-weight: 600; margin-top: 1rem;"),
                ui.tags.div(
                    ui.tags.ul(
                        ui.tags.li(f"Résistance du béton: {safe_get('resistance_mpa', 0, lambda x: f'{x:.2f}')} MPa"),
                        ui.tags.li(f"Résistance structurelle: {safe_get('resistance_structure_mpa', 0, lambda x: f'{x:.2f}')} MPa"),
                        ui.tags.li(f"Type de béton: {projet.get('type_beton', 'N/A')}")
                    ),
                    style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin-bottom: 15px;"
                ),
                
                ui.tags.h5("Déplacement et Déformation", style="color: #0066cc; font-weight: 600; margin-top: 1rem;"),
                ui.tags.div(
                    ui.tags.ul(
                        ui.tags.li(f"Déformation: {safe_get('deformation', 0, lambda x: f'{x:.6f}')}"),
                        ui.tags.li(f"Déplacement estimé: {safe_get('deplacement_mm', 0, lambda x: f'{x:.2f}')} mm")
                    ),
                    style="background-color: #d1ecf1; padding: 15px; border-radius: 5px; margin-bottom: 20px;"
                ),
                
                style="margin-bottom: 30px;"
            ),
            
            # ============================================================
            # SECTION 2: COÛTS ET PLANIFICATION
            # ============================================================
            ui.tags.div(
                ui.tags.h4("2. Coûts et Planification", class_="section-header"),
                
                ui.tags.h5("Détail des Coûts", style="color: #0066cc; font-weight: 600; margin-top: 1rem;"),
                ui.tags.div(
                    ui.tags.h6("Coût des Matériaux:", style="color: #0066cc; font-weight: 600;"),
                    ui.tags.ul(
                        ui.tags.li(f"Ciment: {safe_get('cout_ciment_eur', 0, lambda x: f'{x:.2f}')} €"),
                        ui.tags.li(f"Sable: {safe_get('cout_sable_eur', 0, lambda x: f'{x:.2f}')} €"),
                        ui.tags.li(f"Gravier: {safe_get('cout_gravier_eur', 0, lambda x: f'{x:.2f}')} €"),
                        ui.tags.li(ui.tags.strong(f"Total Matériaux: {safe_get('cout_materiaux_eur', 0, lambda x: f'{x:.2f}')} €", style="color: #0066cc;"))
                    ),
                    style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 15px; border: 1px solid #0066cc;"
                ),
                
                ui.tags.div(
                    ui.tags.h6("Coût de la Main-d'œuvre:", style="color: #0066cc; font-weight: 600;"),
                    ui.tags.ul(
                        ui.tags.li(f"Coût main-d'œuvre: {safe_get('cout_main_oeuvre_eur', 0, lambda x: f'{x:.2f}')} €")
                    ),
                    style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 15px; border: 1px solid #0066cc;"
                ),
                
                ui.tags.div(
                    ui.tags.h6("Coût Total du Projet:", style="color: #0066cc; font-size: 1.2em; font-weight: 600;"),
                    ui.tags.p(
                        ui.tags.strong(f"{safe_get('cout_total_eur', 0, lambda x: f'{x:.2f}')} €", style="font-size: 1.5em; color: #0066cc;"),
                        style="text-align: center; margin: 10px 0;"
                    ),
                    style="background-color: #e8f4f8; padding: 20px; border-radius: 5px; margin-bottom: 15px; border: 2px solid #0066cc;"
                ),
                
                ui.tags.h5("Durée du Projet", style="color: #0066cc; font-weight: 600; margin-top: 1rem;"),
                ui.tags.div(
                    ui.tags.p(
                        ui.tags.strong("Durée estimée: ", style="font-size: 1.1em;"),
                        ui.tags.span(f"{safe_get('duree_projet_jours', 0)} jour(s)", 
                                   style="color: #0066cc; font-size: 1.3em; font-weight: bold;")
                    ),
                    style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 20px;"
                ),
                
                style="margin-bottom: 30px;"
            ),
            
            # ============================================================
            # SECTION 3: ANALYSE DE SÉCURITÉ
            # ============================================================
            ui.tags.div(
                ui.tags.h4("3. Analyse de Sécurité", class_="section-header"),
                
                ui.tags.div(
                    ui.tags.ul(
                        ui.tags.li(f"Charge totale appliquée: {safe_get('charge_totale_kn', 0, lambda x: f'{x:.2f}')} kN"),
                        ui.tags.li(f"Contrainte appliquée: {safe_get('contrainte_mpa', 0, lambda x: f'{x:.2f}')} MPa"),
                        ui.tags.li(f"Résistance du béton: {safe_get('resistance_mpa', 0, lambda x: f'{x:.2f}')} MPa"),
                        ui.tags.li(
                            f"Marge de sécurité: {safe_get('marge_securite', 0, lambda x: f'{x:.2f}')}",
                            style="color: #0066cc; font-weight: bold; font-size: 1.1em;"
                        ),
                        ui.tags.li(f"Coefficient de sécurité requis: {safe_get('coefficient_securite', 1.5, lambda x: f'{x:.2f}')}")
                    ),
                    style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 15px;"
                ),
                
                ui.tags.div(
                    ui.tags.p(
                        "Marge de sécurité insuffisante !" 
                        if safe_get('marge_securite', 0) < safe_get('coefficient_securite', 1.5)
                        else "Marge de sécurité acceptable",
                        style="color: #0066cc; font-weight: bold; padding: 15px; background-color: #e8f4f8; border-radius: 5px; border-left: 4px solid #0066cc;"
                    ),
                    style="margin-bottom: 20px;"
                ),
                
                style="margin-bottom: 30px;"
            ),
            
            # ============================================================
            # SECTION 4: QUANTITÉS DE MATÉRIAUX
            # ============================================================
            ui.tags.div(
                ui.tags.h4("4. Quantités de Matériaux Nécessaires", class_="section-header"),
                
                ui.tags.table(
                    ui.tags.thead(
                        ui.tags.tr(
                            ui.tags.th("Matériau", style="padding: 10px; background-color: #0066cc; color: white;"),
                            ui.tags.th("Quantité", style="padding: 10px; background-color: #0066cc; color: white;"),
                            ui.tags.th("Unité", style="padding: 10px; background-color: #0066cc; color: white;")
                        )
                    ),
                    ui.tags.tbody(
                        ui.tags.tr(
                            ui.tags.td("Ciment", style="padding: 8px; border: 1px solid #ddd;"),
                            ui.tags.td(f"{safe_get('quantite_ciment_kg', 0, lambda x: f'{x:.0f}')}", 
                                     style="padding: 8px; border: 1px solid #ddd; text-align: right;"),
                            ui.tags.td("kg", style="padding: 8px; border: 1px solid #ddd;")
                        ),
                        ui.tags.tr(
                            ui.tags.td("Eau", style="padding: 8px; border: 1px solid #ddd;"),
                            ui.tags.td(f"{safe_get('quantite_eau_kg', 0, lambda x: f'{x:.0f}')}", 
                                     style="padding: 8px; border: 1px solid #ddd; text-align: right;"),
                            ui.tags.td("kg", style="padding: 8px; border: 1px solid #ddd;")
                        ),
                        ui.tags.tr(
                            ui.tags.td("Sable", style="padding: 8px; border: 1px solid #ddd;"),
                            ui.tags.td(f"{safe_get('quantite_sable_kg', 0, lambda x: f'{x:.0f}')}", 
                                     style="padding: 8px; border: 1px solid #ddd; text-align: right;"),
                            ui.tags.td("kg", style="padding: 8px; border: 1px solid #ddd;")
                        ),
                        ui.tags.tr(
                            ui.tags.td("Gravier", style="padding: 8px; border: 1px solid #ddd;"),
                            ui.tags.td(f"{safe_get('quantite_gravier_kg', 0, lambda x: f'{x:.0f}')}", 
                                     style="padding: 8px; border: 1px solid #ddd; text-align: right;"),
                            ui.tags.td("kg", style="padding: 8px; border: 1px solid #ddd;")
                        )
                    ),
                    style="width: 100%; border-collapse: collapse; margin-bottom: 20px;"
                ),
                
                style="margin-bottom: 20px;"
            ),
            
            # ============================================================
            # RÉSUMÉ EXÉCUTIF
            # ============================================================
            ui.tags.div(
                ui.tags.h4("Résumé Exécutif", style="text-align: center; color: #0066cc; margin-top: 30px;"),
                ui.tags.div(
                    ui.layout_columns(
                        ui.tags.div(
                            ui.tags.h5("Volume", style="text-align: center; color: #0066cc;"),
                            ui.tags.p(f"{safe_get('volume_beton_m3', 0, lambda x: f'{x:.2f}')} m³", 
                                    style="text-align: center; font-size: 1.5em; font-weight: bold; color: #0066cc;"),
                            style="background-color: #e8f4f8; padding: 15px; border-radius: 10px; border: 1px solid #0066cc;"
                        ),
                        ui.tags.div(
                            ui.tags.h5("Coût Total", style="text-align: center; color: #0066cc;"),
                            ui.tags.p(f"{safe_get('cout_total_eur', 0, lambda x: f'{x:.0f}')} €", 
                                    style="text-align: center; font-size: 1.5em; font-weight: bold; color: #0066cc;"),
                            style="background-color: #e8f4f8; padding: 15px; border-radius: 10px; border: 1px solid #0066cc;"
                        ),
                        ui.tags.div(
                            ui.tags.h5("Durée", style="text-align: center; color: #0066cc;"),
                            ui.tags.p(f"{safe_get('duree_projet_jours', 0)} jour(s)", 
                                    style="text-align: center; font-size: 1.5em; font-weight: bold; color: #0066cc;"),
                            style="background-color: #e8f4f8; padding: 15px; border-radius: 10px; border: 1px solid #0066cc;"
                        ),
                        ui.tags.div(
                            ui.tags.h5("Sécurité", style="text-align: center; color: #0066cc;"),
                            ui.tags.p(
                                "Attention" if safe_get('marge_securite', 0) < safe_get('coefficient_securite', 1.5) else "OK",
                                style="text-align: center; font-size: 1.5em; font-weight: bold; color: #0066cc;"
                            ),
                            style="background-color: #e8f4f8; padding: 15px; border-radius: 10px; border: 1px solid #0066cc;"
                        ),
                        col_widths=[3, 3, 3, 3]
                    ),
                    style="margin-top: 20px;"
                ),
                style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #ddd;"
            ),
            
            style="background-color: #ffffff; padding: 30px; border-radius: 15px; margin-top: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);"
        )
    
    # ------------------------------------------------------------------------
    # PARTIE III: MODULE ANALYSTE - Analyses Statistiques
    # ------------------------------------------------------------------------
    
    @reactive.calc
    def charger_donnees():
        """Charge les données depuis PostgreSQL - Se met à jour automatiquement"""
        input.submit_btn()
        try:
            print("🔄 Chargement des données depuis PostgreSQL...")
            with engine.connect() as conn:
                query = "SELECT * FROM projets_beton"
                
                # Appliquer le filtre si nécessaire
                if input.filtre_type() != "Tous":
                    query += f" WHERE type_structure = '{input.filtre_type()}'"
                
                df = pd.read_sql(text(query), conn)
                print(f"📊 Données chargées: {len(df)} projets")
                if not df.empty:
                    print(f"📋 Colonnes: {list(df.columns)}")
                return df
        except Exception as e:
            print(f"❌ Erreur de chargement: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    @render.ui
    def stats_summary():
        """Affiche les statistiques globales résumées"""
        df = charger_donnees()
        if df.empty:
            return ui.tags.p("Aucune donnée disponible", style="color: #666; font-weight: 500;")
        
        n_projets = len(df)
        total_volume = df['volume_beton_m3'].sum() if 'volume_beton_m3' in df.columns else 0
        total_cout = df['cout_total_eur'].sum() if 'cout_total_eur' in df.columns else 0
        avg_resistance = df['resistance_mpa'].mean() if 'resistance_mpa' in df.columns else 0
        
        return ui.tags.div(
            ui.tags.h5("📊 Statistiques"),
            ui.tags.p(f"Nombre de projets: {n_projets}"),
            ui.tags.p(f"Volume total: {total_volume:.1f} m³"),
            ui.tags.p(f"Coût total: {total_cout:.0f} €"),
            ui.tags.p(f"Résistance moyenne: {avg_resistance:.1f} MPa")
        )
    
    @render.plot
    def plot_univar():
        """Graphique d'analyse univariée (distribution)"""
        df = charger_donnees()
        var_choisie = input.var_univar()
        
        if df.empty or var_choisie not in df.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "Aucune donnée disponible", ha="center", va="center", fontsize=16)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            return fig
        
        data_clean = df[var_choisie].dropna()
        
        if len(data_clean) == 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "Données insuffisantes", ha="center", va="center", fontsize=16)
            return fig
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sns.histplot(data=data_clean, kde=True, ax=ax, bins=20, color='steelblue', alpha=0.7)
        
        mean_val = data_clean.mean()
        median_val = data_clean.median()
        
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Moyenne: {mean_val:.2f}')
        ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Médiane: {median_val:.2f}')
        
        ax.set_title(f"Distribution de: {var_choisie}", fontsize=16, fontweight='bold')
        ax.set_xlabel(var_choisie, fontsize=12)
        ax.set_ylabel("Fréquence", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return fig
    
    @render.plot
    def plot_bivar():
        """Graphique d'analyse bivariée (corrélation)"""
        df = charger_donnees()
        var1 = input.var_bivar1()
        var2 = input.var_bivar2()
        
        if df.empty or var1 not in df.columns or var2 not in df.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "Aucune donnée disponible", ha="center", va="center", fontsize=16)
            return fig
        
        data_clean = df[[var1, var2]].dropna()
        
        if len(data_clean) == 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "Données insuffisantes", ha="center", va="center", fontsize=16)
            return fig
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sns.scatterplot(data=data_clean, x=var1, y=var2, ax=ax, s=100, alpha=0.6, color='steelblue')
        
        # Calculer et afficher la ligne de régression avec matplotlib directement
        z = np.polyfit(data_clean[var1], data_clean[var2], 1)
        p = np.poly1d(z)
        ax.plot(data_clean[var1], p(data_clean[var1]), "r--", linewidth=2, label="Ligne de régression")
        ax.legend()
        
        ax.set_title(f"Corrélation entre {var1} et {var2}", fontsize=16, fontweight='bold')
        ax.set_xlabel(var1, fontsize=12)
        ax.set_ylabel(var2, fontsize=12)
        ax.grid(True, alpha=0.3)
        
        return fig
    
    @render.text
    def correlation_output():
        """Calcule et affiche les tests de corrélation"""
        df = charger_donnees()
        var1 = input.var_bivar1()
        var2 = input.var_bivar2()
        
        if df.empty or var1 not in df.columns or var2 not in df.columns:
            return "Veuillez sélectionner deux variables valides."
        
        data_clean = df[[var1, var2]].dropna()
        
        if len(data_clean) < 3:
            return f"Données insuffisantes pour calculer la corrélation.\nActuellement: {len(data_clean)} observation(s)\nMinimum requis: 3 observations\nAjoutez {3 - len(data_clean)} projet(s) supplémentaire(s) pour voir les corrélations."
        
        corr_pearson, p_value_pearson = stats.pearsonr(data_clean[var1], data_clean[var2])
        corr_spearman, p_value_spearman = stats.spearmanr(data_clean[var1], data_clean[var2])
        
        if abs(corr_pearson) >= 0.7:
            force = "Forte"
        elif abs(corr_pearson) >= 0.4:
            force = "Modérée"
        elif abs(corr_pearson) >= 0.2:
            force = "Faible"
        else:
            force = "Très faible"
        
        direction = "positive" if corr_pearson > 0 else "négative"
        significatif = "OUI" if p_value_pearson < 0.05 else "NON"
        
        result = f"""
╔══════════════════════════════════════════════════════════════╗
║          RÉSULTATS DES TESTS DE CORRÉLATION                  ║
╚══════════════════════════════════════════════════════════════╝

CORRÉLATION DE PEARSON (Relation Linéaire)
   Coefficient (r): {corr_pearson:.4f}
   P-valeur: {p_value_pearson:.4f}
   Force: {force} | Direction: {direction}
   Statistiquement significatif (α=0.05): {significatif}

CORRÉLATION DE SPEARMAN (Relation Monotone)
   Coefficient (ρ): {corr_spearman:.4f}
   P-valeur: {p_value_spearman:.4f}

Interprétation:
   • Ces corrélations mesurent la relation entre {var1} et {var2}.
   • Une valeur proche de 1 ou -1 indique une relation forte.
   • Une corrélation n'implique PAS une relation causale.

Application Génie Civil:
   • Relation positive forte: Les deux variables augmentent ensemble
   • Relation négative: Quand une variable augmente, l'autre diminue
   • Exemple: Volume béton vs Coût total (relation positive attendue)

Nombre d'observations utilisées: {len(data_clean)}
        """
        
        return result


# ============================================================================
# CRÉATION DE L'APPLICATION
# ============================================================================

# Créer l'application au niveau du module pour que Railway puisse la trouver
app = App(app_ui, server)

# Lancer l'application seulement si exécutée directement (développement local)
if __name__ == "__main__":
    app.run(port=8000, reload=False)

