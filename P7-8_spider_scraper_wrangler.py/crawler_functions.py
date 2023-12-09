import requests
from bs4 import BeautifulSoup
import csv
import json
import unicodedata

def remove_non_ascii(text):
    return ''.join(char for char in text if ord(char) < 128)

def get_university_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find_all("table", class_="infobox vcard")

def process_data_item(data_item):
    return remove_non_ascii(unicodedata.normalize("NFKD", data_item.get_text().strip()))

def extract_data(header_text, data_item, data):
    header_key = header_text.lower().replace(' ', '_').replace('in\xa0', '_')
    if data_item:
        try:
            data[header_key] = int(process_data_item(data_item))
        except ValueError:
            data[header_key] = process_data_item(data_item).split(';')[0]
    else:
        data[header_key] = None

def scrape_university_data(reader):
    data_list = []

    for country_name, url_country, name_of_university, url_university in reader:
        target_tables = get_university_data(url_university)

        if target_tables:
            target_table = target_tables[0]
        else:
            print(f"No table with class 'infobox vcard' found for {name_of_university}")
            continue

        data = {'country_name': country_name, 'name_of_university': name_of_university}

        images = target_table.find_all('img')
        if images:
            data['seal'] = images[0]['src']
            data['logo'] = images[-1]['src']
        else:
            print(f"No image with tag 'img' found for {name_of_university}")

        rows = target_table.find_all('tr')
        for row in rows:
            header = row.find('th')
            if header:
                header_text = header.text.strip()
                data_item = row.find('td')
                extract_data(header_text, data_item, data)

                # The rest of your code for processing header_text goes here

        data_list.append(data)

    return data_list

def save_to_json(data_list, filename):
    with open(filename, 'w') as json_file:
        json.dump(data_list, json_file, indent=4)

def main():
    file = open('universities.csv', 'r')
    reader = csv.reader(file)
    next(reader)  # Skip the header row

    data_list = scrape_university_data(reader)

    save_to_json(data_list, 'german_universities_data.json')

    file.close()

if __name__ == "__main__":
    main()
