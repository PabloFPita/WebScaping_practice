import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def extract_countries(soup, head_of_url):
    country_dict = {}
    link_elements = soup.find_all('li')

    for link_element in link_elements:
        anchor_tag = link_element.find('a')
        if anchor_tag and anchor_tag.has_attr('href') and "List of universities" in anchor_tag.get('title', ''):
            country_name = anchor_tag.get_text(strip=True)
            country_link = anchor_tag['href']
            absolute_link = urljoin(head_of_url, country_link)
            country_dict[country_name] = absolute_link

    return country_dict

def save_countries_to_csv(country_dict, filename):
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Country', 'Link'])

        for key, value in country_dict.items():
            writer.writerow([key, value])

def load_countries_from_csv(filename):
    country_matrix = []

    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        country_matrix = list(reader)

    return country_matrix

def find_country_url(country_matrix, country_to_look_for):
    for country_row in country_matrix:
        country_name = country_row.get('Country')
        if country_name and country_name == country_to_look_for:
            return country_row.get('Link')

    return None

def scrape_universities(url_germany):
    response_germany = requests.get(url_germany)

    if response_germany.status_code == 200:
        soup_germany = BeautifulSoup(response_germany.content, 'html.parser')
        german_universities_dict = {}
        anchor_tags = soup_germany.select('ul:not(.gallery) a[title][href]')
        start_flag = False
        stop_flag = False

        for anchor_tag in anchor_tags:
            german_uni_name = anchor_tag['title']
            german_uni_link = anchor_tag['href']

            if german_uni_name == "RWTH Aachen":
                start_flag = True

            if start_flag:
                absolute_link_german_uni = urljoin(url_germany, german_uni_link)
                german_universities_dict[german_uni_name] = absolute_link_german_uni

            if german_uni_name == "University of Würzburg":
                stop_flag = True

            if stop_flag:
                break

        return german_universities_dict

    else:
        print(f"Error al descargar la página de Alemania. Código de estado: {response_germany.status_code}")
        return None

def save_universities_to_csv(german_universities_dict, country_to_look_for, url_germany, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['country_name', 'url-country', 'name_of_university', 'url_university']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for uni_name, uni_link in german_universities_dict.items():
            writer.writerow({
                'country_name': country_to_look_for,
                'url-country': url_germany,
                'name_of_university': uni_name,
                'url_university': uni_link
            })

        print(f"CSV '{filename}' creado exitosamente.")

def main():
    url = "https://en.wikipedia.org/wiki/Lists_of_universities_and_colleges_by_country"
    head_of_url = "https://en.wikipedia.org"
    soup = get_soup(url)
    
    country_dict = extract_countries(soup, head_of_url)
    save_countries_to_csv(country_dict, 'countries.csv')

    country_matrix = load_countries_from_csv('countries.csv')

    country_to_look_for = 'Germany'
    url_germany = find_country_url(country_matrix, country_to_look_for)

    if url_germany:
        german_universities_dict = scrape_universities(url_germany)

        if german_universities_dict:
            save_universities_to_csv(german_universities_dict, country_to_look_for, url_germany, 'universities.csv')
    else:
        print("No se encontró la URL de Alemania en la matriz.")

if __name__ == "__main__":
    main()
