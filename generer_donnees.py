import csv
import random

# Départements et leurs régions
data_structure = {
    "Adamaoua": ["Djerem", "Faro-et-Deo", "Mayo-Banyo", "Mbere", "Vina"],
    "Centre": ["Haute-Sanaga", "Lekie", "Mbam-et-Inoubou", "Mbam-et-Kim", "Mefou-et-Afamba", "Mefou-et-Akono", "Mfoundi", "Nyong-et-Kelle", "Nyong-et-Mfoumou", "Nyong-et-So'o"],
    "Est": ["Boumba-et-Ngoko", "Haut-Nyong", "Kadey", "Lom-et-Djerem"],
    "Extreme-Nord": ["Diamare", "Logone-et-Chari", "Mayo-Danay", "Mayo-Kani", "Mayo-Sava", "Mayo-Tsanaga"],
    "Littoral": ["Moungo", "Nkam", "Sanaga-Maritime", "Wouri"],
    "Nord": ["Benoue", "Faro", "Mayo-Louti", "Mayo-Rey"],
    "Nord-Ouest": ["Boyo", "Bui", "Donga-Mantung", "Menchum", "Mezam", "Momo", "Ngo-Ketunjia"],
    "Ouest": ["Bamboutos", "Haut-Nkam", "Hauts-Plateaux", "Koung-Khi", "Menoua", "Mifi", "Nde", "Noun"],
    "Sud": ["Dja-et-Lobo", "Mvila", "Ocean", "Vallee-du-Ntem"],
    "Sud-Ouest": ["Fako", "Koupe-Manengouba", "Lebialem", "Manyu", "Meme", "Ndian"]
}

# Départements ayant accès à la pêche (Mer ou grands fleuves/lacs)
zones_peche = ["Wouri", "Sanaga-Maritime", "Fako", "Ndian", "Ocean", "Logone-et-Chari", "Mayo-Danay", "Benoue"]

def generate_prod(liste_choix, base_vol):
    # Choisir 3 produits au hasard dans la liste sans doublons
    choix = random.sample(liste_choix, 3)
    # Générer des volumes décroissants (le 1er est le dominant)
    v1 = base_vol + random.randint(0, 5000)
    v2 = int(v1 * 0.6) # Le 2ème produit fait 60% du premier
    v3 = int(v1 * 0.3) # Le 3ème fait 30%
    return choix, [v1, v2, v3]

def get_data(dept, region):
    # Configuration par zone agro-écologique
    if region in ["Extreme-Nord", "Nord", "Adamaoua"]:
        cultures = ["Coton", "Sorgho", "Oignon", "Arachide", "Maïs", "Mil"]
        elevages = ["Bovins", "Caprins", "Ovins", "Volailles"]
        vol_agri = 15000
        vol_elev = 50000
    elif region in ["Ouest", "Nord-Ouest"]:
        cultures = ["Café Arabica", "Maïs", "Pomme de terre", "Haricot", "Tomate", "Carotte"]
        elevages = ["Volailles", "Porcins", "Lapins", "Caprins"]
        vol_agri = 12000
        vol_elev = 20000
    else: # Grand Sud forestier
        cultures = ["Cacao", "Café Robusta", "Banane-Plantain", "Manioc", "Huile de Palme", "Hévéa"]
        elevages = ["Porcins", "Volailles", "Pisciculture", "Petits Ruminants"]
        vol_agri = 25000
        vol_elev = 5000

    # Génération Agriculture
    c_noms, c_vols = generate_prod(cultures, vol_agri)
    
    # Génération Élevage
    e_noms, e_vols = generate_prod(elevages, vol_elev)

    # Génération Pêche
    peche_type = "Aucune"
    peche_vol = 0
    if dept in zones_peche:
        peche_type = "Pêche Artisanale Maritime" if region in ["Littoral", "Sud", "Sud-Ouest"] else "Pêche Continentale"
        peche_vol = random.randint(1000, 15000)

    return [
        dept, region,
        c_noms[0], c_vols[0], c_noms[1], c_vols[1], c_noms[2], c_vols[2],
        e_noms[0], e_vols[0], e_noms[1], e_vols[1], e_noms[2], e_vols[2],
        peche_type, peche_vol
    ]

# Écriture du CSV
filename = "donnees_agricoles_completes.csv"
print(f"Génération de {filename}...")

with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    # En-tête (Headres)
    writer.writerow([
        "nom_dept", "nom_region",
        "agri_1", "vol_agri_1", "agri_2", "vol_agri_2", "agri_3", "vol_agri_3",
        "elev_1", "vol_elev_1", "elev_2", "vol_elev_2", "elev_3", "vol_elev_3",
        "peche_type", "vol_peche"
    ])
    
    for region, depts in data_structure.items():
        for dept in depts:
            writer.writerow(get_data(dept, region))

print("Terminé ! Données riches générées.")
