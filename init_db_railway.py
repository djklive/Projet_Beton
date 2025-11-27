"""
Script d'initialisation de la base de données PostgreSQL sur Railway
Exécutez ce script une seule fois après avoir déployé sur Railway

Usage:
    railway run python init_db_railway.py
"""

from sqlalchemy import create_engine, text
import os
from urllib.parse import quote_plus

print("=" * 60)
print("Initialisation de la base de données PostgreSQL")
print("=" * 60)

# Récupérer DATABASE_URL depuis les variables d'environnement Railway
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ ERREUR: DATABASE_URL n'est pas définie")
    print("Vérifiez que vous avez ajouté un service PostgreSQL dans Railway")
    exit(1)

# Adapter l'URL pour psycopg2
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

print(f"✅ DATABASE_URL trouvée")
print(f"📊 Connexion à la base de données...")

try:
    engine = create_engine(DATABASE_URL, echo=False)
    
    # Lire le script SQL
    sql_file = "create_table_genie_civil.sql"
    if not os.path.exists(sql_file):
        print(f"❌ ERREUR: Fichier {sql_file} introuvable")
        exit(1)
    
    print(f"📄 Lecture du fichier {sql_file}...")
    with open(sql_file, "r", encoding="utf-8") as f:
        sql_script = f.read()
    
    # Vérifier si la table existe déjà
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'projets_beton'
            );
        """))
        table_exists = result.fetchone()[0]
        
        if table_exists:
            print("⚠️  La table 'projets_beton' existe déjà")
            response = input("Voulez-vous la supprimer et la recréer ? (oui/non): ")
            if response.lower() in ['oui', 'o', 'yes', 'y']:
                print("🗑️  Suppression de la table existante...")
                conn.execute(text("DROP TABLE IF EXISTS projets_beton CASCADE;"))
                conn.commit()
                print("✅ Table supprimée")
            else:
                print("❌ Opération annulée. La table existante est conservée.")
                exit(0)
        
        # Exécuter le script SQL
        print("🚀 Exécution du script SQL...")
        conn.execute(text(sql_script))
        conn.commit()
        print("✅ Script SQL exécuté avec succès")
        
        # Vérifier que la table a été créée
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'projets_beton'
            );
        """))
        table_exists = result.fetchone()[0]
        
        if table_exists:
            print("✅ Table 'projets_beton' créée avec succès")
            
            # Vérifier les colonnes
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'projets_beton'
                ORDER BY ordinal_position;
            """))
            columns = [row[0] for row in result.fetchall()]
            print(f"📋 Colonnes créées ({len(columns)}): {', '.join(columns[:5])}...")
        else:
            print("❌ ERREUR: La table n'a pas été créée")
            exit(1)

except Exception as e:
    print(f"❌ ERREUR lors de l'initialisation: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("=" * 60)
print("🎉 Initialisation terminée avec succès!")
print("=" * 60)

