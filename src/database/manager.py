import os
import psycopg2

class DatabaseManager:
    def __init__(self):
        self.conn_params = {
            "host": os.getenv("DB_HOST", "localhost"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASS"),
            "port": os.getenv("DB_PORT", "5432")
        }

    def _get_connection(self):
        return psycopg2.connect(**self.conn_params)

    def init_db(self):
        """Crée la table avec les 7 colonnes de ton modèle + le prix prédit."""
        query = """
        CREATE TABLE IF NOT EXISTS historique_predictions (
            id SERIAL PRIMARY KEY,
            date_prediction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            surface_habitable FLOAT,
            prix_m2_moyen FLOAT,
            longitude FLOAT,
            latitude FLOAT,
            est_appartement INTEGER,
            nb_transactions_precedent INTEGER,
            mois_transaction INTEGER,
            prix_predit FLOAT
        );
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                conn.commit()
            return True
        except Exception:
            return False

    def save_prediction(self, data_dict, prix_final):
        """Prend le dictionnaire de données et le prix pour les sauvegarder."""
        query = """
        INSERT INTO historique_predictions (
            surface_habitable, prix_m2_moyen, longitude, latitude, 
            est_appartement, nb_transactions_precedent, mois_transaction, prix_predit
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (
            data_dict['surface_habitable'][0],
            data_dict['prix_m2_moyen_mois_precedent'][0],
            data_dict['longitude'][0],
            data_dict['latitude'][0],
            data_dict['type_batiment_Appartement'][0],
            data_dict['nb_transactions_mois_precedent'][0],
            data_dict['mois_transaction'][0],
            float(prix_final)
        )
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, values)
                conn.commit()
                conn.close()
            return True
        except Exception as e:
            print(f"Erreur DB: {e}")
            return False

# Test rapide si on lance ce fichier directement
if __name__ == "__main__":
    db = DatabaseManager()
    
    print("--- Test 1 : Initialisation ---")
    db.init_db()
    
    print("--- Test 2 : Insertion d'une donnée fictive ---")
    data_test = {
        'surface_habitable': [75.0],
        'prix_m2_moyen_mois_precedent': [5000.0],
        'longitude': [2.35],
        'latitude': [48.85],
        'type_batiment_Appartement': [1],
        'nb_transactions_mois_precedent': [50],
        'mois_transaction': [12]
    }
    
    success = db.save_prediction(data_test, 375000.0)
    
    if success:
        print("✅ Insertion réussie !")
    else:
        print("❌ Échec de l'insertion.")