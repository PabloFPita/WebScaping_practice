import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def scrape_url(url, nameCompany, nameOferta):
    data = {}
    # Initialize ChromeDriver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    # Cerrar ventana de cookies
    cookies = driver.find_element(By.XPATH, '//*[@id="cookiesSize"]/div[2]/button[2]')
    cookies.click()
    time.sleep(1)

    # Locate the table
    table = driver.find_element(By.XPATH, "//table")

    # Iterate through each row in the table
    for row in table.find_elements(By.XPATH, "//tr"):
        # Extract data from the cells in each row
        cells = row.find_elements(By.XPATH, ".//td")
        
        # Check if there are at least two cells (name and value)
        if len(cells) >= 2:
            name = cells[0].text.strip()
            value = cells[1].text.strip()
            
            # Add the data to the dictionary
            data[name] = value

    write_dictionary(data, nameCompany, nameOferta)
    # Close the browser
    driver.close()

    return data

def write_dictionary(data, nameCompany, nameOferta):
    # Create a dictionary to store company, offer names, and scraped data
    result = {
        'Company Name': nameCompany,
        'Offer Name': nameOferta,
        'Data': data
    }

    # Write the data to a JSON file
    with open('P9-10_Selenium\datos_diccionario.json', 'a', encoding='utf-8-sig') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)



def main():
    print("Starting the crawler...")
    # Read the urls from the file
    df = pd.read_csv('P9-10_Selenium\ofertas_electricidad_functions.csv', sep=',', header=0)

    urls = df['URL de la Oferta'].tolist()
    nameCompanies = df['Denominación Social Empresa Comercializadora'].tolist()
    nameOfertas = df['Denominación de la Oferta'].tolist()

    # Use zip to iterate over multiple lists simultaneously
    for url, nameCompany, nameOferta in zip(urls, nameCompanies, nameOfertas):
        scrape_url(url, nameCompany, nameOferta)

if __name__ == "__main__":
    main()
