import sys
from bs4 import BeautifulSoup
import requests
import time
import datetime

import os
from os.path import exists
from datetime import datetime


def go_to_date(date):
    try:
        formatted_date = datetime.strptime(date, "%Y%m%d").strftime("%Y/%m/%d")
        url = f"https://www.boe.es/borme/dias/{formatted_date}/index.php?s=A"
        print(f"Downloading from date: {url}")
        time.sleep(2)
        find_pdfs(url)
    except Exception as e:
        print(f"An error occurred with the date: {str(e)}")


def find_pdfs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))
    for link in pdf_links:
        pdf_url = link['href']
        pdf_url = f"https://www.boe.es{pdf_url}"
        filename = pdf_url.split('/')[-1]
        download_pdf(pdf_url, filename)


def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        # Create the directory if it does not exist
        absolute_path = "C:\\Users\\pablo\\Documents\\MasterBigData\\AdquisicionTransformacion\\PracticasPython\\P11_Borne\\"
        directory = absolute_path + year + "\\" + month + "\\" + day + "\\"
        if not exists(directory):
            os.makedirs(directory)
            print(f"Directory {directory} created")
        time.sleep(2)
        # Si el filename contiene BORME-S- en vez de BORME-A-, no lo descargamos
        if "BORME-S-" in filename:
            print(f"File {filename} not downloaded. Boletín de Sociedades")
            return
        # Write the file
        with open(directory + filename, "wb") as output_file:
            print(f"Writing file {filename}")
            output_file.write(response.content)


def get_dates(date):
    global year, month, day
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    go_to_date(date)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 spyder.py YYYYMMDD or python3 spyder.py input_file.txt")
        sys.exit(1)
    
    input_arg = sys.argv[1]
    
    if input_arg.endswith(".txt"):
        with open(input_arg, "r") as file:
            dates = file.readlines()
            for date in dates:
                date = date.strip()
                get_dates(date)
    else:
        date = input_arg
        get_dates(date)


if __name__ == "__main__":
    main()