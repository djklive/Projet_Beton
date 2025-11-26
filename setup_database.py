"""
Script de configuration et vérification de la base de données
Exécutez ce script pour vérifier que tout est configuré correctement
"""

from sqlalchemy import create_engine, text, inspect
import pandas as pd

# Configuration - MODIFIEZ SELON VOS IDENTIFIANTS
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/db_patients"

def check_database():
    """Vérifie et configure la base de données"""
    try:
        # Connexion à la base
        engine = create_engine(DATABASE_URL)
        
        print("🔄 Connexion à PostgreSQL...")
        with engine.connect() as conn:
            # Vérifier si la table existe
            inspector = inspect(engine)
            if 'dossiers_patients' not in inspector.get_table_names():
                print("❌ La table 'dossiers_patients' n'existe pas !")
                print("📝 Veuillez créer la table via pgAdmin ou exécuter le script SQL fourni.")
                return False
            
            print("✅ Table 'dossiers_patients' trouvée")
            
            # Vérifier les colonnes
            columns = inspector.get_columns('dossiers_patients')
            column_names = [col['name'] for col in columns]
            
            print(f"\n📊 Colonnes actuellement dans la table:")
            for col in columns:
                print(f"   - {col['name']}: {col['type']}")
            
            # Vérifier si la colonne imc existe
            if 'imc' not in column_names:
                print("\n⚠️  Colonne 'imc' manquante. Ajout en cours...")
                conn.execute(text("ALTER TABLE dossiers_patients ADD COLUMN imc NUMERIC(5, 2)"))
                conn.commit()
                print("✅ Colonne 'imc' ajoutée avec succès")
            else:
                print("✅ Colonne 'imc' existe déjà")
            
            # Compter les enregistrements
            result = conn.execute(text("SELECT COUNT(*) FROM dossiers_patients"))
            count = result.fetchone()[0]
            print(f"\n📈 Nombre d'enregistrements: {count}")
            
            if count > 0:
                print("\n📋 Premier enregistrement (exemple):")
                df = pd.read_sql(text("SELECT * FROM dossiers_patients LIMIT 1"), conn)
                print(df.to_string(index=False))
            
        print("\n✅ Base de données correctement configurée !")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la vérification: {e}")
        print("\n💡 Vérifiez:")
        print("   1. PostgreSQL est démarré")
        print("   2. Les identifiants dans ce fichier sont corrects")
        print("   3. La base 'db_patients' existe")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 Vérification de la configuration de la base de données")
    print("=" * 60)
    check_database()
    print("=" * 60)

