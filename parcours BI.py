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
    df.to_csv('objectif_bi.csv', index=False, encoding='utf-8')

    print("Les objectifs ont été enregistrés dans le fichier 'objectif_bi.csv'.")
else:
    print("Aucun objectif spécifique pour le parcours BI trouvé.")


# Find the <h3> tag with text "Contenu"
contenu_section = soup.find('h3', text="Contenu")

# Print "Contenu" text
print("Contenu:")

# Find the <ul> and <p> elements that are directly after the <h3> tag
content = contenu_section.find_all_next(['ul', 'p'], limit=8)

# Print the extracted content
for tag in content:
    print(tag.get_text(strip=True))



# Find the <h3> tag with text "Compétences"
competences_section = soup.find('h3', text="Compétences")

# Print "Compétences" text
print("Compétences:")

# Find the <ul> element directly after the "Compétences" heading
competences_list = competences_section.find_next('ul')

# Print each item in the list
for item in competences_list.find_all('li'):
    print(item.get_text(strip=True))




# Extract the "Métiers" section
metiers_section = soup.find('h3', text="Métiers")
if metiers_section:
    print("Métiers:")
    metiers_list = metiers_section.find_next('ul')
    for item in metiers_list.find_all('li'):
        print(item.get_text(strip=True))

# Extract the "Secteurs d’activité" section
secteurs_section = soup.find('h3', text="Secteurs d’activité")
if secteurs_section:
    print("\nSecteurs d’activité:")
    secteurs_list = secteurs_section.find_next('ul')
    for item in secteurs_list.find_all('li'):
        print(item.get_text(strip=True))

# Extract the "Partenariats professionnels" section
partenariats_section = soup.find('h3', text="Partenariats professionnels")
if partenariats_section:
    print("\nPartenariats professionnels:")
    # Look for the <div> that contains the partnership info and extract <p> tags
    partenariats_paragraphs = partenariats_section.find_next('div', class_="stage").find_all('p')
    for para in partenariats_paragraphs:
        print(para.get_text(strip=True))




# Define the semester ids to target
semester_ids = [
    "elementor-tab-content-4181",  # Semestre 1
    "elementor-tab-content-4182",  # Semestre 2
    "elementor-tab-content-4183",  # Semestre 3
    "elementor-tab-content-4184",  # Semestre 4
    "elementor-tab-content-4185",  # Semestre 5
]

# Loop through each semester and extract the subjects
for semester_id in semester_ids:
    semestre = soup.find('div', id=semester_id)
    if semestre:
        subjects_list = semestre.find_all('li')
        semester_name = semestre.find_previous('a').get_text(strip=True)  # Extract the semester name
        print(f"\n{semester_name}:")
        for item in subjects_list:
            print(item.get_text(strip=True))