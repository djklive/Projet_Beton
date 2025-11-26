"""
Application de Collecte et d'Analyse de Données Patients
Développée avec Shiny for Python et PostgreSQL

Modules:
    - Module Infirmière: Saisie des données patient
    - Module Médecin: Analyse statistique (univariée, bivariée, corrélations)
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
# ⚠️ ATTENTION: Modifiez ces valeurs selon votre configuration
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "Djoko002&"  # Votre mot de passe (peut contenir &)
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB = "db_patients"

# Encoder le mot de passe pour gérer les caractères spéciaux comme &
encoded_password = quote_plus(POSTGRES_PASSWORD)
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{encoded_password}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL, echo=False)

# Test de connexion au démarrage
print("🔌 Test de connexion à PostgreSQL...")
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"✅ Connexion PostgreSQL réussie! Version: {version[:50]}...")
        
        # Vérifier que la table existe
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'dossiers_patients'
            );
        """))
        table_exists = result.fetchone()[0]
        if table_exists:
            print("✅ Table 'dossiers_patients' existe")
            
            # Vérifier les colonnes
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'dossiers_patients'
                ORDER BY ordinal_position;
            """))
            columns = [row[0] for row in result.fetchall()]
            print(f"✅ Colonnes disponibles: {columns}")
            
            # Vérifier si la colonne imc existe
            if 'imc' in columns:
                print("✅ Colonne 'imc' existe")
            else:
                print("⚠️  Colonne 'imc' MANQUANTE - Veuillez exécuter add_column_imc.sql")
        else:
            print("❌ Table 'dossiers_patients' N'EXISTE PAS - Veuillez exécuter create_table.sql")
except Exception as e:
    print(f"❌ ERREUR DE CONNEXION: {e}")
    print("⚠️  Vérifiez vos identifiants PostgreSQL et que le serveur est démarré")
    import traceback
    traceback.print_exc()

# Configuration du style des graphiques
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_theme(style="darkgrid", palette="husl")

# ============================================================================
# INTERFACE UTILISATEUR (UI) - Module Infirmière
# ============================================================================

ui_infirmiere = ui.nav_panel(
    "📝 Saisie Infirmière",
    ui.tags.h2("Module de Collecte de Données Patient"),
    ui.tags.p("Remplissez le formulaire ci-dessous pour enregistrer une nouvelle visite patient."),
    ui.tags.br(),
    
    # Section Identité du Patient
    ui.tags.h4("Identité du Patient"),
    ui.input_text("patient_ref_id", "Référence Patient", "PAT-001", width="300px"),
    ui.input_date("date_naissance", "Date de Naissance", value=str(datetime.date(1990, 1, 1))),
    ui.input_radio_buttons("sexe", "Sexe", {"Homme": "Homme", "Femme": "Femme", "Autre": "Autre"}),
    
    ui.tags.hr(),
    
    # Section Signes Vitaux
    ui.tags.h4("Signes Vitaux (Visite du Jour)"),
    ui.input_numeric("poids_kg", "Poids (kg)", value=70.0, min=0, max=300, step=0.1),
    ui.input_numeric("taille_cm", "Taille (cm)", value=175.0, min=0, max=250, step=0.1),
    ui.input_numeric("tension_systolique", "Tension Systolique (mmHg)", value=120, min=50, max=250),
    ui.input_numeric("tension_diastolique", "Tension Diastolique (mmHg)", value=80, min=30, max=150),
    ui.input_numeric("temperature_celsius", "Température (°C)", value=37.0, min=32.0, max=45.0, step=0.1),
    
    ui.tags.hr(),
    
    # Bouton de soumission
    ui.input_action_button("submit_btn", "💾 Enregistrer la Visite", class_="btn-primary btn-lg"),
    
    ui.tags.br(), ui.tags.br(),
    
    # Zone de messages
    ui.output_text_verbatim("submit_message_output"),
    ui.output_ui("imc_calculated")
)

# ============================================================================
# INTERFACE UTILISATEUR (UI) - Module Médecin
# ============================================================================

ui_medecin = ui.nav_panel(
    "📊 Tableau de Bord Médecin",
    ui.tags.h2("Analyse des Données Patients"),
    ui.tags.p("Sélectionnez les variables à analyser dans les menus ci-dessous."),
    
    ui.layout_sidebar(
        ui.sidebar(
            # Section Analyse Univariée
            ui.tags.h5("📈 Analyse Univariée"),
            ui.input_select(
                "var_univar",
                "Variable (Distribution)",
                {
                    "poids_kg": "Poids (kg)",
                    "taille_cm": "Taille (cm)",
                    "temperature_celsius": "Température (°C)",
                    "tension_systolique": "Tension Systolique (mmHg)",
                    "tension_diastolique": "Tension Diastolique (mmHg)",
                    "imc": "IMC (Indice de Masse Corporelle)"
                },
                selected="poids_kg"
            ),
            
            ui.tags.hr(),
            
            # Section Analyse Bivariée
            ui.tags.h5("🔗 Analyse Bivariée (Corrélation)"),
            ui.input_select(
                "var_bivar1",
                "Variable X",
                {
                    "poids_kg": "Poids (kg)",
                    "taille_cm": "Taille (cm)",
                    "tension_systolique": "Tension Syst.",
                    "tension_diastolique": "Tension Diast.",
                    "temperature_celsius": "Température",
                    "imc": "IMC"
                },
                selected="poids_kg"
            ),
            ui.input_select(
                "var_bivar2",
                "Variable Y",
                {
                    "poids_kg": "Poids (kg)",
                    "taille_cm": "Taille (cm)",
                    "tension_systolique": "Tension Syst.",
                    "tension_diastolique": "Tension Diast.",
                    "temperature_celsius": "Température",
                    "imc": "IMC"
                },
                selected="taille_cm"
            ),
            
            ui.tags.hr(),
            
            # Statistiques globales
            ui.output_ui("stats_summary"),
            
            width=300
        ),
        
        # Graphique Univarié
        ui.tags.h4("Distribution Univariée"),
        ui.output_plot("plot_univar", height="400px"),
        
        ui.tags.br(), ui.tags.br(),
        
        # Graphique Bivarié
        ui.tags.h4("Analyse de Corrélation (Bivariée)"),
        ui.output_plot("plot_bivar", height="400px"),
        
        ui.tags.br(), ui.tags.br(),
        
        # Résultats des tests statistiques
        ui.tags.h4("Tests de Corrélation"),
        ui.output_text_verbatim("correlation_output"),
    )
)

# ============================================================================
# UI PRINCIPALE - Application avec Navigation par Onglets
# ============================================================================

app_ui = ui.page_navbar(
    ui_infirmiere,
    ui_medecin,
    title="🏥 Dossier Patient Numérique",
    sidebar=None
)

# ============================================================================
# LOGIQUE SERVEUR (SERVER)
# ============================================================================

def server(input, output, session):
    """Fonction serveur contenant toute la logique de l'application"""
    
    # Variables réactives pour stocker les messages
    submit_message = reactive.Value("")
    imc_message = reactive.Value(ui.tags.p(""))
    
    # ------------------------------------------------------------------------
    # PARTIE I: MODULE INFIRMIÈRE - Enregistrement des Données
    # ------------------------------------------------------------------------
    
    @reactive.Effect
    @reactive.event(input.submit_btn)
    def handle_submission():
        """Gère l'enregistrement des données patient dans PostgreSQL"""
        print("🔄 BOUTON CLIQUE - Début de l'enregistrement...")
        try:
            # Calcul de l'IMC (Indice de Masse Corporelle)
            poids = input.poids_kg()
            taille_m = input.taille_cm() / 100.0  # Conversion cm -> mètres
            imc = 0.0
            if taille_m > 0 and poids > 0:
                imc = poids / (taille_m ** 2)
            
            print(f"📊 Données calculées - Poids: {poids}, Taille: {input.taille_cm()}, IMC: {imc:.2f}")
            
            # Création du dictionnaire de données
            new_data = {
                "patient_ref_id": input.patient_ref_id(),
                "date_naissance": input.date_naissance(),
                "sexe": input.sexe(),
                "poids_kg": input.poids_kg(),
                "taille_cm": input.taille_cm(),
                "tension_systolique": input.tension_systolique(),
                "tension_diastolique": input.tension_diastolique(),
                "temperature_celsius": input.temperature_celsius(),
                "imc": round(imc, 2)  # Arrondi à 2 décimales
            }
            
            print(f"📦 Données préparées: {new_data}")
            
            # Conversion en DataFrame Pandas
            df = pd.DataFrame([new_data])
            
            print("💾 Tentative d'écriture dans PostgreSQL...")
            
            # Écriture dans PostgreSQL (corrigé pour SQLAlchemy 2.0)
            with engine.begin() as conn:
                df.to_sql('dossiers_patients', conn, if_exists='append', index=False)
            
            print("✅ DONNÉES ENREGISTRÉES AVEC SUCCÈS DANS POSTGRESQL!")
            
            # Message de succès
            msg = f"✅ Patient {input.patient_ref_id()} enregistré avec succès !"
            print(f"📝 Message de succès: {msg}")
            ui.notification_show(msg, duration=5, type="success")
            submit_message.set(msg)
            
            # Afficher l'IMC calculé
            imc_msg = f"💡 IMC calculé: {imc:.2f} kg/m²"
            if imc < 18.5:
                interpretation = " (Insuffisance pondérale)"
            elif imc < 25:
                interpretation = " (Poids normal)"
            elif imc < 30:
                interpretation = " (Surpoids)"
            else:
                interpretation = " (Obésité)"
            imc_message.set(ui.tags.p(imc_msg + interpretation, style="color: #0066cc; font-weight: bold;"))
            print(f"📊 IMC affiché: {imc_msg}{interpretation}")
            
        except Exception as e:
            error_msg = f"❌ Erreur lors de l'enregistrement : {str(e)}"
            print(f"❌ ERREUR DÉTAILLÉE: {e}")
            print(f"❌ Type d'erreur: {type(e).__name__}")
            import traceback
            print(f"❌ Traceback complet:")
            traceback.print_exc()
            ui.notification_show(error_msg, duration=10, type="error")
            submit_message.set(error_msg)
            imc_message.set(ui.tags.p(""))
    
    # Fonction pour afficher le message de soumission
    @render.text
    @reactive.event(input.submit_btn)  # Déclencher le re-render quand le bouton est cliqué
    def submit_message_output():
        return submit_message()
    
    # Fonction pour afficher l'IMC calculé
    @render.ui
    @reactive.event(input.submit_btn)  # Déclencher le re-render quand le bouton est cliqué
    def imc_calculated():
        return imc_message()
    
    # ------------------------------------------------------------------------
    # PARTIE II: MODULE MÉDECIN - Analyses Statistiques
    # ------------------------------------------------------------------------
    
    @reactive.calc
    def charger_donnees():
        """Charge les données depuis PostgreSQL - Se met à jour automatiquement"""
        # Déclencher le rechargement quand le bouton submit est cliqué
        input.submit_btn()
        try:
            print("🔄 Chargement des données depuis PostgreSQL...")
            with engine.connect() as conn:
                df = pd.read_sql(text("SELECT * FROM dossiers_patients"), conn)
                print(f"📊 Données chargées: {len(df)} enregistrements")
                if not df.empty:
                    print(f"📋 Colonnes: {list(df.columns)}")
                    print(f"📋 Première ligne: {df.iloc[0].to_dict()}")
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
            return ui.tags.p("⚠️ Aucune donnée disponible", style="color: orange;")
        
        n_patients = len(df)
        n_hommes = len(df[df['sexe'] == 'Homme'])
        n_femmes = len(df[df['sexe'] == 'Femme'])
        
        return ui.tags.div(
            ui.tags.h5("📊 Statistiques"),
            ui.tags.p(f"Nombre total de patients: {n_patients}"),
            ui.tags.p(f"Hommes: {n_hommes}"),
            ui.tags.p(f"Femmes: {n_femmes}")
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
        
        # Filtrer les valeurs nulles
        data_clean = df[var_choisie].dropna()
        
        if len(data_clean) == 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "Données insuffisantes", ha="center", va="center", fontsize=16)
            return fig
        
        # Création du graphique
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Histogramme avec courbe de densité
        sns.histplot(data=data_clean, kde=True, ax=ax, bins=20, color='steelblue', alpha=0.7)
        
        # Statistiques descriptives
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
        
        # Filtrer les valeurs nulles
        data_clean = df[[var1, var2]].dropna()
        
        if len(data_clean) == 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "Données insuffisantes", ha="center", va="center", fontsize=16)
            return fig
        
        # Création du graphique
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Nuage de points avec ligne de régression
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
            return "⚠️ Veuillez sélectionner deux variables valides."
        
        # Filtrer les valeurs nulles
        data_clean = df[[var1, var2]].dropna()
        
        if len(data_clean) < 3:
            return f"⚠️ Données insuffisantes pour calculer la corrélation.\n📊 Actuellement: {len(data_clean)} observation(s)\n📊 Minimum requis: 3 observations\n💡 Ajoutez {3 - len(data_clean)} patient(s) supplémentaire(s) dans l'onglet 'Saisie Infirmière' pour voir les corrélations."
        
        # Calcul de la corrélation de Pearson
        corr_pearson, p_value_pearson = stats.pearsonr(data_clean[var1], data_clean[var2])
        
        # Calcul de la corrélation de Spearman
        corr_spearman, p_value_spearman = stats.spearmanr(data_clean[var1], data_clean[var2])
        
        # Interprétation de Pearson
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
        
        # Construction du message de résultats
        result = f"""
╔══════════════════════════════════════════════════════════════╗
║          RÉSULTATS DES TESTS DE CORRÉLATION                  ║
╚══════════════════════════════════════════════════════════════╝

📊 CORRÉLATION DE PEARSON (Relation Linéaire)
   Coefficient (r): {corr_pearson:.4f}
   P-valeur: {p_value_pearson:.4f}
   Force: {force} | Direction: {direction}
   Statistiquement significatif (α=0.05): {significatif}

📈 CORRÉLATION DE SPEARMAN (Relation Monotone)
   Coefficient (ρ): {corr_spearman:.4f}
   P-valeur: {p_value_spearman:.4f}

📝 Interprétation:
   • Ces corrélations mesurent la relation entre {var1} et {var2}.
   • Une valeur proche de 1 ou -1 indique une relation forte.
   • Une corrélation n'implique PAS une relation causale.

Nombre d'observations utilisées: {len(data_clean)}
        """
        
        return result


# ============================================================================
# LANCEMENT DE L'APPLICATION
# ============================================================================

if __name__ == "__main__":
    app = App(app_ui, server)
    app.run(port=8000, reload=False)

