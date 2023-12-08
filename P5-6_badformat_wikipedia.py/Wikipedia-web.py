import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Comillas_Pontifical_University"
response = requests.get(url)
print(response.status_code)

soup = BeautifulSoup(response.content, "html.parser")

target_tables = soup.find_all("table", class_="infobox vcard")
print(len(target_tables))
print(soup.title)
target_table = target_tables[0]

data = {}

images = target_table.find_all('img')
data['seal'] = images[0]['src']
data['logo'] = images[-1]['src']

rows = target_table.find_all('tr')
for row in rows:
    header = row.find('th')
    if header:
        header_text = header.text.strip()
        data_item = row.find('td')
        if data_item:
            data_item = data_item.get_text().strip() # Extract the text from the element
            try:
                data[header_text.lower().replace(' ', '_').replace('in\xa0', '_')] = int(data_item)
            except ValueError:
                data[header_text.lower().replace(' ', '_').replace('in\xa0', '_')] = data_item.split(';')[0]
        else:
            data[header_text.lower().replace(' ', '_').replace('in\xa0', '_')] = None
    else:
        continue
    if header_text == 'Motto Latin:':
        header_text = header_text.split('Latin: ')[1]
        data_item = data_item.split(' (')[0]
        data['motto_latin'] = data_item
        data.pop('motto_latin:')
    if header_text == 'Motto':
        data['motto_spanish'] = data_item
        data.pop('motto')
    if header_text == 'Motto in English':
        data['motto_english'] = data_item
        data.pop('motto_in_english')
    if header_text == 'Established':
        data_item = data_item.split(',')[0]
        data['established'] = data_item
    if header_text == 'Rector':
        data_item = data_item.split('[')[0]
        data['rector'] = data_item
    if header_text == 'Students':
        data_item = data_item.replace(',', '.')
        data['students'] = data_item

print(data)
