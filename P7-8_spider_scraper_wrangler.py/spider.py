import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

url = "https://en.wikipedia.org/wiki/Lists_of_universities_and_colleges_by_country"
head_of_url = "https://en.wikipedia.org"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

# Find all <a> tags within <li> tags
link_elements = soup.find_all('li')

# Create a dictionary to store country names and links
country_dict = {}

# Extract country names and links for anchors with titles containing "List of universities"
for link_element in link_elements:
    anchor_tag = link_element.find('a')  # Check if <li> contains <a>
    if anchor_tag and anchor_tag.has_attr('href') and "List of universities" in anchor_tag.get('title', ''):
        country_name = anchor_tag.get_text(strip=True)
        country_link = anchor_tag['href']
        # Construct the absolute URL by joining the base URL and the relative link
        absolute_link = urljoin(head_of_url, country_link)
        
        country_dict[country_name] = absolute_link
 
# Now create a csv file out of the dictionary
with open('countries.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    # Write the header, Country and Link
    writer.writerow(['Country', 'Link'])
    for key, value in country_dict.items():
        writer.writerow([key, value])


country_matrix = []
# Abre el archivo CSV y carga la matriz
with open('countries.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    country_matrix = list(reader)

country_to_look_for = 'Germany'
url_germany = None
# Bucle para analizar la matriz country_matrix fila a fila
for country_row in country_matrix:
    country_name = country_row.get('Country')
    # Condición para evaluar la lógica del nuevo spider solo cuando el nombre del país sea "Alemania" (Germany)
    if country_name and country_name == country_to_look_for:
        # Aquí colocarás la lógica específica para extraer las URLs de Alemania
        # Puedes acceder a otras columnas de la fila utilizando country_row['Nombre de la Columna']
        print(f"Analyzing data for {country_name}")
        url_germany = country_row.get('Link')


# Verifica si se encontró la URL de Alemania
if url_germany:
    # Descarga el HTML de la URL de Alemania
    response_germany = requests.get(url_germany)
    if response_germany.status_code == 200:
        # Parséa el HTML con BeautifulSoup
        soup_germany = BeautifulSoup(response_germany.content, 'html.parser')

        # Encuentra los nombre de la universidad (el title de los <a> tags) y las URLs de las universidades (el href de los <a> tags)
        german_universities_dict = {}

        # Find all <a> tags inside <ul> tags that don't have class "gallery"
        anchor_tags = soup_germany.select('ul:not(.gallery) a[title][href]')

        # Flags to indicate when to start and stop adding to the dictionary
        start_flag = False
        stop_flag = False

        # Iterate through <a> elements
        for anchor_tag in anchor_tags:
            german_uni_name = anchor_tag['title']
            german_uni_link = anchor_tag['href']

            # Check if the title is "RWTH Aachen" to start adding to the dictionary
            if german_uni_name == "RWTH Aachen":
                start_flag = True

            # Add to the dictionary if the start flag is True
            if start_flag:
                # Construct the absolute URL by joining the base URL and the relative link
                absolute_link_german_uni = urljoin(url_germany, german_uni_link)
                german_universities_dict[german_uni_name] = absolute_link_german_uni

            if german_uni_name == "University of Würzburg":
                stop_flag = True

            if stop_flag:
                break

        # Imprime un CSV llamado "universities.csv" con la estructura especificada
        csv_filename = "universities.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['country_name', 'url-country', 'name_of_university', 'url_university']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Escribe la fila de encabezado
            writer.writeheader()

            # Escribe los datos de las universidades en el CSV
            for uni_name, uni_link in german_universities_dict.items():
                writer.writerow({
                    'country_name': country_to_look_for,
                    'url-country': url_germany,
                    'name_of_university': uni_name,
                    'url_university': uni_link
                })

            print(f"CSV '{csv_filename}' creado exitosamente.")
    else:
        print(f"Error al descargar la página de Alemania. Código de estado: {response_germany.status_code}")
else:
    print("No se encontró la URL de Alemania en la matriz.")