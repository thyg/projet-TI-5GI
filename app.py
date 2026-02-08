from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import json
import os

app = Flask(__name__)
CORS(app)

#def get_db_connection():
 #   conn = psycopg2.connect(
  #      host="127.0.0.1",
   #     database="cameroun_db",
    #    user="jude",
     #   password="123456789", # Ton mot de passe validé
      #  port="5432"          # Ton port validé
    #)
    #return conn


def get_db_connection():
    # Récupère l'URL de la base sécurisée fournie par Render
    db_url = os.environ.get('DATABASE_URL')
    
    if db_url:
        # Connexion Cloud (Render)
        conn = psycopg2.connect(db_url)
    else:
        # Connexion Locale (Ton PC - Sécurité au cas où)
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="cameroun_db",
            user="jude",
            password="123456789",
            port="5432"
        )
    return conn


@app.route('/')
def home():
    return "<h1>Serveur SIG Cameroun En Ligne</h1>"

@app.route('/api/donnees', methods=['GET'])
def get_donnees():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # LA REQUÊTE COMPLÈTE (celle qui correspond à ton site web)
        query = """
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', json_agg(json_build_object(
                'type', 'Feature',
                'geometry', ST_AsGeoJSON(geom)::json,
                'properties', json_build_object(
                    'nom', nom,
                    'region', nom_region,
                    'agri_1', agri_1, 'vol_agri_1', vol_agri_1,
                    'agri_2', agri_2, 'vol_agri_2', vol_agri_2,
                    'agri_3', agri_3, 'vol_agri_3', vol_agri_3,
                    'elev_1', elev_1, 'vol_elev_1', vol_elev_1,
                    'elev_2', elev_2, 'vol_elev_2', vol_elev_2,
                    'elev_3', elev_3, 'vol_elev_3', vol_elev_3,
                    'peche_type', peche_type, 'vol_peche', vol_peche
                )
            ))
        )
        FROM vue_globale;
        """
        
        cur.execute(query)
        result = cur.fetchone()
        
        if result is None or result[0] is None:
            return jsonify({"error": "Pas de données"}), 404
            
        data = result[0]
        cur.close()
        conn.close()
        
        return jsonify(data)
    
    except Exception as e:
        print(f"ERREUR SQL: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
