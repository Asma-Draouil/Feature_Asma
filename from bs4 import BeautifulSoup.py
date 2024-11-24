from bs4 import BeautifulSoup
import requests
import csv 
def get_page_contents(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    page = requests.get(url, headers=headers)

    if page.status_code == 200:
        return page.text

    return None
def get_school_programs(page_contents):
    soup = BeautifulSoup(page_contents, 'html.parser')
    structured_content = {}
    
    # Find the main div containing the sections
    parcours_compta_div = soup.find('div', id='elementor-tab-content-7522', class_='elementor-tab-content elementor-clearfix')
    
    if parcours_compta_div:
        # Find all h3 headings within this div
        headings = parcours_compta_div.find_all('h3')
        
        for heading in headings:
            key_text = heading.get_text(strip=True)
            
            # Handle 'Matières par semestre' specially
            if key_text == 'Matières par semestre':
                semester_content = {}
                
                for i in range(1, 7):  # Loop through semesters 1 to 6
                    semester_heading = heading.find_next(string=f'Semestre {i}')
                    
                    if semester_heading:
                        # Get the <ul> list that follows the semester heading
                        materials_list = semester_heading.find_next('ul')
                        materials = [li.get_text(strip=True) for li in materials_list.find_all('li')] if materials_list else []
                        
                        # Add to the dictionary for the current semester
                        semester_content[f'Semestre {i}'] = materials
                
                # Add the gathered semester content to the main dictionary under 'Matières par semestre'
                structured_content['Matières par semestre'] = semester_content
            
            else:
                # Collect both <p> and <ul> elements following the heading
                values = []
                for sibling in heading.find_next_siblings(['p', 'ul']):
                    if sibling.name == 'p':
                        values.append(sibling.get_text(strip=True))
                    elif sibling.name == 'ul':
                        # Extract text from all <li> elements in the <ul>
                        values.extend([li.get_text(strip=True) for li in sibling.find_all('li')])
                
                structured_content[key_text] = values
    
    return structured_content
if __name__ == '__main__':
    url = 'https://www.esb.tn/programmes/licences/sciences-de-gestion/'
    page_contents = get_page_contents(url)
    result=[]   #keep result when appending all of the programs for now we will try to use it for csv test file

    if page_contents:
        result.append(get_school_programs(page_contents))
    else:
        print('Failed to get page contents.')
field_names = [
    'Objectifs', 'Contenu', 'Compétences', 'Métiers', 'Secteurs d’activité', 'Partenariats professionnels',
    'Semestre 1', 'Semestre 2', 'Semestre 3', 'Semestre 4', 'Semestre 5', 'Semestre 6'
]

# Flatten the data
flattened_result = {}
for dict in result:
    for key, value in dict.items():
        if key == 'Matières par semestre':
            # Extract each semester as a separate field
            for semester, courses in value.items():
                flattened_result[semester] = ', '.join(courses)
        elif isinstance(value, list):
            # Join list items with commas
            flattened_result[key] = ', '.join(value)
        else:
            flattened_result[key] = value

# Write to CSV
with open('programs.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    
    # Write the header
    writer.writeheader()
    
    # Write the flattened result as a row
    writer.writerow(flattened_result)