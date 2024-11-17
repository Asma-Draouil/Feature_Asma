import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la page web
url = 'https://www.esb.tn/programmes/licences/licence-en-business-computing/'

# Charger le contenu HTML depuis la page web
response = requests.get(url)
response.raise_for_status()  # Vérifier que la requête s'est bien passée
html_content = response.text

# Parser le contenu avec Beautiful Soup
soup = BeautifulSoup(html_content, 'html.parser')

# Extraire l'objectif du parcours BI
# On recherche les éléments contenant le mot "BI" et vérifie le contexte
objective_bi = []
for element in soup.find_all(string=lambda text: "BI" in text if text else False):
    parent = element.find_parent()
    if parent and 'objectif' in parent.get_text().lower():
        # Extraire seulement la phrase contenant l'objectif souhaité
        full_text = parent.get_text(strip=True)
        target_text = "L’objectif est de former des consultants dotés d’une assise théorique et technique solide leur permettant de concevoir, développer et exploiter des applications décisionnelles.Ce parcours est disponible en double diplôme en Systèmes d’Information et Aide à la Décision avec l’Université"
        if target_text in full_text:
            objective_bi.append(target_text)

# Afficher le résultat
if objective_bi:
    # Créer un DataFrame à partir de la liste
    df = pd.DataFrame(objective_bi, columns=['Objectif BI'])

    # Exporter vers un fichier CSV
    df.to_csv('objectif_bi.csv', index=False, encoding='utf-8-sig')

    print("Les objectifs ont été enregistrés dans le fichier 'objectif_bi.csv'.")
else:
    print("Aucun objectif spécifique pour le parcours BI trouvé.")


# Trouver la balise <h3> avec le texte "Contenu"
contenu_section = soup.find('h3', text="Contenu")

# Vérifier si la section a été trouvée
if contenu_section:
    print("Contenu:")

    # Trouver les éléments <ul> et <p> qui suivent directement
    content = contenu_section.find_all_next(['ul', 'p'], limit=8)

    # Extraire le texte de chaque élément et le stocker dans une liste
    content_list = [tag.get_text(strip=True) for tag in content]

    # Afficher le contenu extrait (facultatif)
    for item in content_list:
        print(item)

    # Créer un DataFrame à partir de la liste
    df = pd.DataFrame(content_list, columns=['Contenu'])

    # Exporter le DataFrame en fichier CSV
    df.to_csv('contenu_extrait.csv', index=False, encoding='utf-8-sig')

    print("Le contenu a été enregistré dans le fichier 'contenu_extrait.csv'.")
else:
    print("Section 'Contenu' non trouvée.")


# Trouver la balise <h3> avec le texte "Compétences"
competences_section = soup.find('h3', text="Compétences")

# Vérifier si la section a été trouvée
if competences_section:
    print("Compétences:")

    # Trouver la balise <ul> qui suit directement le titre "Compétences"
    competences_list = competences_section.find_next('ul')

    # Extraire chaque élément de la liste <li>
    competences = [item.get_text(strip=True) for item in competences_list.find_all('li')]

    # Afficher les compétences extraites (facultatif)
    for competence in competences:
        print(competence)

    # Créer un DataFrame avec les compétences
    df = pd.DataFrame(competences, columns=['Compétences'])

    # Exporter les compétences en fichier CSV
    df.to_csv('competences_extraites.csv', index=False, encoding='utf-8-sig')

    print("Les compétences ont été enregistrées dans le fichier 'competences_extraites.csv'.")
else:
    print("Section 'Compétences' non trouvée.")




# Extraire la section "Métiers"
metiers_section = soup.find('h3', text="Métiers")

# Vérifier si la section a été trouvée
if metiers_section:
    print("Métiers:")

    # Trouver la balise <ul> qui suit directement le titre "Métiers"
    metiers_list = metiers_section.find_next('ul')

    # Extraire chaque élément de la liste <li>
    metiers = [item.get_text(strip=True) for item in metiers_list.find_all('li')]

    # Afficher les métiers extraits (facultatif)
    for metier in metiers:
        print(metier)

    # Créer un DataFrame avec les métiers
    df = pd.DataFrame(metiers, columns=['Métiers'])

    # Exporter les métiers en fichier CSV
    df.to_csv('metiers_extraits.csv', index=False, encoding='utf-8-sig')

    print("Les métiers ont été enregistrés dans le fichier 'metiers_extraits.csv'.")
else:
    print("Section 'Métiers' non trouvée.")



# Extraire la section "Secteurs d’activité"
secteurs_section = soup.find('h3', text="Secteurs d’activité")

# Vérifier si la section a été trouvée
if secteurs_section:
    print("\nSecteurs d’activité:")

    # Trouver la balise <ul> qui suit directement le titre "Secteurs d’activité"
    secteurs_list = secteurs_section.find_next('ul')

    # Extraire chaque élément de la liste <li>
    secteurs = [item.get_text(strip=True) for item in secteurs_list.find_all('li')]

    # Afficher les secteurs extraits (facultatif)
    for secteur in secteurs:
        print(secteur)

    # Créer un DataFrame avec les secteurs
    df = pd.DataFrame(secteurs, columns=['Secteurs d’activité'])

    # Exporter les secteurs en fichier CSV
    df.to_csv('secteurs_activite_extraits.csv', index=False, encoding='utf-8-sig')

    print("Les secteurs d’activité ont été enregistrés dans le fichier 'secteurs_activite_extraits.csv'.")
else:
    print("Section 'Secteurs d’activité' non trouvée.")


# Extraire la section "Partenariats professionnels"
partenariats_section = soup.find('h3', text="Partenariats professionnels")

# Vérifier si la section a été trouvée
if partenariats_section:
    print("\nPartenariats professionnels:")

    # Trouver la balise <div> contenant les informations de partenariat et extraire les <p> tags
    partenariats_paragraphs = partenariats_section.find_next('div', class_="stage").find_all('p')

    # Extraire le texte de chaque paragraphe
    partenariats = [para.get_text(strip=True) for para in partenariats_paragraphs]

    # Afficher les partenariats extraits (facultatif)
    for partenariat in partenariats:
        print(partenariat)

    # Créer un DataFrame avec les partenariats
    df = pd.DataFrame(partenariats, columns=['Partenariats professionnels'])

    # Exporter les partenariats en fichier CSV
    df.to_csv('partenariats_professionnels_extraits.csv', index=False, encoding='utf-8-sig')

    print("Les partenariats professionnels ont été enregistrés dans le fichier 'partenariats_professionnels_extraits.csv'.")
else:
    print("Section 'Partenariats professionnels' non trouvée.")




# Définir les IDs des semestres à cibler
semester_ids = [
    "elementor-tab-content-4181",  # Semestre 1
    "elementor-tab-content-4182",  # Semestre 2
    "elementor-tab-content-4183",  # Semestre 3
    "elementor-tab-content-4184",  # Semestre 4
    "elementor-tab-content-4185",  # Semestre 5
]

# Liste pour stocker les matières et leur semestre
semesters_data = []

# Parcourir chaque semestre et extraire les matières
for semester_id in semester_ids:
    semestre = soup.find('div', id=semester_id)
    if semestre:
        subjects_list = semestre.find_all('li')
        semester_name = semestre.find_previous('a').get_text(strip=True)  # Extraire le nom du semestre
        print(f"\n{semester_name}:")
        
        # Extraire chaque matière et l'ajouter à la liste avec le nom du semestre
        for item in subjects_list:
            subject = item.get_text(strip=True)
            semesters_data.append({'Semestre': semester_name, 'Matière': subject})
            print(subject)

# Créer un DataFrame avec les données des semestres
df = pd.DataFrame(semesters_data)

# Exporter les matières par semestre en fichier CSV
df.to_csv('matieres_par_semestre.csv', index=False, encoding='utf-8-sig')

print("Les matières par semestre ont été enregistrées dans le fichier 'matieres_par_semestre.csv'.")