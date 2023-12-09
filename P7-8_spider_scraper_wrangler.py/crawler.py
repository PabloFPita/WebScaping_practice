import requests
from bs4 import BeautifulSoup
import csv
import json
import unicodedata

def remove_non_ascii(text):
    return ''.join(char for char in text if ord(char) < 128)

file = open('universities.csv', 'r')
reader = csv.reader(file)
next(reader)  # Skip the header row

data_list = []  # Create an empty list to store the data dictionaries

for country_name, url_country, name_of_university, url_university in reader:  # Loop through the csv file
    response = requests.get(url_university)  # Get the response from the university URL
    soup = BeautifulSoup(response.content, "html.parser")  # Parse the response content

    target_tables = soup.find_all("table", class_="infobox vcard")
    if target_tables:  # Check if the list is not empty
        target_table = target_tables[0]  # Get the first element
        # Do something with the target table
    else:
        print("No table with class 'infobox vcard' found")  # Print an error message
        continue  # Move to the next iteration if no target table is found

    data = {}  # Create an empty dictionary to store the data

    images = target_table.find_all('img')
    if images:  # Check if the list is not empty
        data['seal'] = images[0]['src']
        data['logo'] = images[-1]['src']
    else:
        print("No image with tag 'img' found")  # Print an error message

    rows = target_table.find_all('tr')
    for row in rows:
        header = row.find('th')
        if header:
            header_text = header.text.strip()
            data_item = row.find('td')
            if data_item:
                data_item = remove_non_ascii(unicodedata.normalize("NFKD", data_item.get_text().strip()))  # Normalize and remove non-ASCII characters
                try:
                    data[header_text.lower().replace(' ', '_').replace('in\xa0', '_')] = int(data_item)
                except ValueError:
                    data[header_text.lower().replace(' ', '_').replace('in\xa0', '_')] = data_item.split(';')[0]
            else:
                data[header_text.lower().replace(' ', '_').replace('in\xa0', '_')] = None
        else:
            continue

    data['country_name'] = country_name  # Add the country name to the data dictionary
    data['name_of_university'] = name_of_university  # Add the university name to the data dictionary

    data_list.append(data)  # Append the data dictionary to the data list

json_file = open('german_universities_data.json', 'w')  # Open a json file to write the data list
json.dump(data_list, json_file, indent=4)  # Write the data list to the json file
file.close()  # Close the csv file
json_file.close()  # Close the json file
