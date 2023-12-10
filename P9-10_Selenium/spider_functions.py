from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import csv

def navigate_cnmc(driver):
    # Cerrar ventana de cookies
    cookies = driver.find_element(By.XPATH, '//*[@id="cookiesSize"]/div[2]/button[2]')
    cookies.click()
    time.sleep(1)

    open_box = driver.find_element(By.XPATH, '//*[@id="principal"]/div/form/div/div/div[2]/div[2]/div/div[1]/div[1]')
    open_box.click()
    time.sleep(1)

    # Seleccionar la opción de "Electricidad" que esta posicionada la primera en el inputbox
    electricidad = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div/div[1]/div')
    electricidad.click()
    time.sleep(2)

    iniciar = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/main/div/div/div/div/div/div/button/span')
    iniciar.click()
    time.sleep(7)

    codigo_postal = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/main/div/div/div/form/div/div/div/div[1]/div[3]/div[1]/div')
    codigo_postal.click()
    # Fill the codigo_postal input
    codigo_postal_input = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/main/div/div/div/form/div/div/div/div[1]/div[3]/div[1]/div/div/div[1]/div/input')
    time.sleep(2)
    codigo_postal_input.send_keys("28013")
    time.sleep(1)

    continuar = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/main/div/div/div/form/div/div/div/div[2]/button')
    continuar.click()
    time.sleep(20)



def scrape_table(driver):
    tabla = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/main/div/div/div/div/div[2]/div/div[2]/div[1]/div/table')
    filas = tabla.find_elements(By.TAG_NAME, 'tr')
    filas = [fila for fila in filas if fila.get_attribute('class') != 'filtro']

    data = []
    for fila in filas:
        columnas = fila.find_elements(By.TAG_NAME, 'td')
        fila_datos = []
        for columna in columnas:
            try:
                # If it is the first column, get the alt of the image
                img = columna.find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'img')
                fila_datos.append(img.get_attribute('alt'))
                # Once it has been found, continue with the next column
                continue
            except NoSuchElementException:
                pass

            try: 
                div_inside_table = columna.find_element(By.TAG_NAME, 'div')
                # For the "verde" column
                if 'mdi-tree theme--light grey--text' in div_inside_table.find_element(By.TAG_NAME, 'i').get_attribute('class'):
                    fila_datos.append('No')
                # For the "grey" column
                elif 'mdi-tree theme--light green--text' in div_inside_table.find_element(By.TAG_NAME, 'i').get_attribute('class'):
                    fila_datos.append('Sí')                
                # Once it has been found, continue with the next column
                continue
            except NoSuchElementException:
                pass

            try:
                # If it is the last column, get the href of the link
                a_element = columna.find_element(By.TAG_NAME, 'a')
                if a_element.get_attribute('aria-label') == 'Ver oferta':
                    fila_datos.append(a_element.get_attribute('href'))
                elif columna.text:
                    fila_datos.append(columna.text)
            except NoSuchElementException:
                # It is a standard text column
                fila_datos.append(columna.text)
                pass

        data.append(fila_datos)
    return data


def write_table(file_path, data):
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Denominación Social Empresa Comercializadora', 'Denominación de la Oferta',
                         'Importe primeras facturas en Euros', 'Importe siguientes facturas en Euros',
                         'Validez', 'Servicios Adicionales Incluidos', 'Penalización', 'Verde', 'URL de la Oferta'])
        for fila in data:
            writer.writerow(fila)
    time.sleep(1)

def main():
    driver = webdriver.Chrome()

    url_cnmc = "https://comparador.cnmc.gob.es/"
    driver.get(url_cnmc)
    time.sleep(2)

    navigate_cnmc(driver)

    data_from_table = scrape_table(driver)

    write_table('P9-10_Selenium\ofertas_electricidad_functions.csv', data_from_table)

    driver.close()

if __name__ == "__main__":
    main()
