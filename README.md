Voici le contenu complet à copier-coller dans ton fichier README.md.

code
Markdown
download
content_copy
expand_less
# 🇨🇲 Webmapping des Bassins de Production au Cameroun (SIG Web)

![Statut](https://img.shields.io/badge/Statut-Terminé-success)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Stack](https://img.shields.io/badge/Stack-PostGIS%20|%20Flask%20|%20Leaflet-green)

Application de cartographie interactive (WebGIS) développée dans le cadre du projet **5GI (2025-2026)**. Elle permet de visualiser et d'analyser les données de production économique (Agriculture, Élevage, Pêche) à l'échelle des départements du Cameroun.

---

## 🚀 Fonctionnalités Clés

*   **Visualisation Spatiale** : Carte interactive des 58 départements (Données GADM).
*   **Multi-thématique** : Bascule dynamique entre trois couches :
    *   🌱 Agriculture (Dominance et volumes).
    *   🐄 Élevage (Types de cheptels).
    *   🐟 Pêche (Zones maritimes et continentales).
*   **Analyse de Données** :
    *   Popups riches affichant le **TOP 3** des filières pour chaque zone.
    *   Carte choroplèthe (couleurs graduées selon l'intensité de la production).
*   **Expérience Utilisateur (UX)** :
    *   Barre de recherche avec autocomplétion.
    *   Zoom automatique et survol interactif.

---

## 🛠 Architecture Technique

Le projet repose sur une architecture **3-Tiers** légère, privilégiant la flexibilité du code Python sur la lourdeur des serveurs cartographiques Java.

1.  **Niveau Données (Data Layer)**
    *   **SGBD** : PostgreSQL 18 (Cluster main).
    *   **Cartouche Spatiale** : PostGIS (Gestion des géométries vectorielles).
    *   **Données** : Jointure SQL (`vue_globale`) entre les polygones administratifs et les statistiques agricoles.

2.  **Niveau Application (Backend API)**
    *   **Langage** : Python 3.12.
    *   **Framework** : Flask.
    *   **Rôle** : Sert d'API REST. Exécute les requêtes spatiales et convertit les résultats en **GeoJSON** via `ST_AsGeoJSON`.

3.  **Niveau Présentation (Frontend)**
    *   **Librairie** : Leaflet.js (Rendu cartographique côté client).
    *   **Interface** : HTML5 / CSS3 natif.

---

## ⚙️ Installation et Configuration (Ubuntu 24.04)

Guide détaillé pour déployer l'application, incluant les correctifs de sécurité PostgreSQL rencontrés.

### 1. Pré-requis Système
```bash
sudo apt update
sudo apt install python3-pip python3-venv libpq-dev postgresql postgresql-contrib postgis
2. Configuration Critique de PostgreSQL

Sur Ubuntu 24.04, plusieurs versions de PostgreSQL peuvent coexister (16 et 18), créant des conflits de ports et d'authentification.

A. Identifier le bon cluster et le port

code
Bash
download
content_copy
expand_less
pg_lsclusters
# Repérez le port de la version active (ex: 5433 pour la v18 ou 5432 pour la v16)

B. Forcer l'authentification locale (Fix "Password Auth Failed")
PostgreSQL refuse parfois les connexions locales par mot de passe. Nous modifions le fichier pg_hba.conf pour faire confiance à 127.0.0.1.

Commandes automatiques (remplacez /18/ par votre version si nécessaire) :

code
Bash
download
content_copy
expand_less
# Remplace la méthode 'scram-sha-256' ou 'md5' par 'trust' pour localhost
sudo sed -i '/127.0.0.1\/32/s/scram-sha-256/trust/' /etc/postgresql/18/main/pg_hba.conf
sudo sed -i '/127.0.0.1\/32/s/md5/trust/' /etc/postgresql/18/main/pg_hba.conf

# Redémarrage du service pour appliquer
sudo systemctl restart postgresql

C. Initialisation de la Base de Données

code
Bash
download
content_copy
expand_less
# Connexion en spécifiant le port (ex: -p 5433)
sudo -u postgres psql -p 5433

# Commandes SQL :
CREATE DATABASE cameroun_db;
\c cameroun_db
CREATE EXTENSION postgis;
ALTER USER postgres WITH PASSWORD '123456789'; -- Définition du mot de passe
\q
3. Importation des Données

A. Import des Shapefiles (Géométrie)

code
Bash
download
content_copy
expand_less
# Utilisation de shp2pgsql pour envoyer les contours dans la base
shp2pgsql -I -s 4326 data/gadm41_CMR_2.shp departements | sudo -u postgres psql -p 5433 -d cameroun_db

B. Génération et Import des Données Agricoles

Générer le CSV simulé :

code
Bash
download
content_copy
expand_less
python3 generer_donnees.py

Contourner les droits d'accès PostgreSQL (Fix "Permission Denied") :

code
Bash
download
content_copy
expand_less
cp donnees_agricoles_completes.csv /tmp/
chmod 777 /tmp/donnees_agricoles_completes.csv

Exécuter le script SQL de création de tables et de la vue (voir fichier schema.sql ou documentation interne).

4. Démarrage de l'Application

Activer l'environnement virtuel :

code
Bash
download
content_copy
expand_less
python3 -m venv venv
source venv/bin/activate

Installer les dépendances :

code
Bash
download
content_copy
expand_less
pip install flask flask-cors psycopg2-binary

Lancer le serveur :

code
Bash
download
content_copy
expand_less
python3 app.py

Note : Vérifiez dans app.py que port="5433" (ou votre port Postgres) est bien configuré.

Accès : Ouvrir index.html dans un navigateur.

🔄 Alternative Technique : Remplacer Python par GeoServer

Le cahier des charges mentionnait GeoServer. Bien que nous ayons choisi Python (Flask) pour sa rapidité de développement et sa gestion native du JSON personnalisé, voici comment la migration s'effectuerait :

Pourquoi GeoServer ?

GeoServer est un serveur cartographique standard OGC. Il permet de publier des données sans écrire de code backend, via une interface graphique.

Procédure de Migration :

Installation : Installer Java (default-jdk) et déployer GeoServer (Tomcat ou Binaires).

Connexion SGBD :

Dans l'interface GeoServer (localhost:8080/geoserver), créer un nouvel Entrepôt de données (Store) de type "PostGIS".

Connecter à la base cameroun_db sur le port 5433.

Publication (Layer) :

Publier la table vue_globale.

Configurer le système de coordonnées (SRS) en EPSG:4326.

Consommation Frontend (Le changement majeur) :

Le fichier app.py devient inutile et est supprimé.

Dans index.html, l'URL de fetch doit être modifiée pour interroger le standard WFS (Web Feature Service) de GeoServer :

code
JavaScript
download
content_copy
expand_less
// Ancienne URL (Python API)
// fetch('http://127.0.0.1:5000/api/donnees')

// Nouvelle URL (GeoServer WFS)
const url = "http://localhost:8080/geoserver/wfs?service=WFS&version=1.1.0&request=GetFeature&typeName=cameroun:vue_globale&outputFormat=application/json";

fetch(url).then(...)
Pourquoi ne pas l'avoir fait ?

La configuration des règles CORS (Cross-Origin Resource Sharing) sur GeoServer nécessite l'édition complexe de fichiers XML (web.xml) et le redémarrage du serveur Java, ce qui ajoutait une complexité inutile pour un prototype de 4 jours, comparé à la simplicité de CORS(app) dans Flask.

📂 Structure du Répertoire
code
Bash
download
content_copy
expand_less
.
├── app.py                      # Backend API (Flask)
├── generer_donnees.py          # Script de génération de données (Mock data)
├── index.html                  # Frontend (Carte Leaflet)
├── data/                       # Shapefiles bruts (GADM)
├── README.md                   # Documentation technique
└── venv/                       # Environnement virtuel Python (exclu du git)
👤 Auteur

Projet réalisé par Wotchoko.

code
Code
download
content_copy
expand_less
