# Importar librería requests
import requests
import csv
import sys

# Clave de API de AEMET
# Haz que tengas que pasarla como argumento al script
if len(sys.argv) < 2:
    print("Please provide the API key as the first argument when executing the script.")
    sys.exit(1)

api_key = sys.argv[1]

# Por defecto buscamos solo en Madrid, Ciudad Universitaria. Podríamos hacer que esto fuese otro parámetro de entrada del script.
estacion_buscada = "MADRID, CIUDAD UNIVERSITARIA"
# Define las fechas de inicio y fin para octubre de 2019
fecha_ini = "2019-10-01T00:00:00UTC"
fecha_fin = "2019-11-01T00:00:00UTC"

# URL de la API de AEMET
url_all_stations = f"https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"

# Llamar a la API de AEMET para obtener los datos con la clave de API
response_1 = requests.get(url_all_stations, params={'api_key': api_key})

# Check if the request was successful (status code 200)
if response_1.status_code == 200:

    # Download the actual data from the provided URL
    data_response_2 = requests.get(response_1.json()["datos"])

    # Check if the data request was successful
    if data_response_2.status_code == 200:
        # The data is in JSON format
        all_stations = data_response_2.json()
        indicativo = next((entry["indicativo"] for entry in all_stations if entry["nombre"] == estacion_buscada), None)
        if indicativo:
            print(f"Indicativo: {indicativo}")

        # URL de la API de AEMET para obtener los datos de climatologías diarias
        climatologia_url = f"https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{fecha_ini}/fechafin/{fecha_fin}/estacion/{indicativo}"

        # Realizar la solicitud GET al endpoint de climatologías diarias
        response_climatologia_3 = requests.get(climatologia_url, params={'api_key': api_key})

        if response_climatologia_3.status_code == 200:
            # Descargar los datos reales desde el enlace proporcionado
            url_datos_4 = requests.get(response_climatologia_3.url)

            if url_datos_4.status_code == 200:
                print("URL para obtener los datos deseados:",url_datos_4.json()['datos'])
                # Descargar los datos reales desde el enlace proporcionado
                data_response_5 = requests.get(url_datos_4.json()['datos'])

                if data_response_5.status_code == 200:
                    # Los datos de climatología diaria están en formato JSON
                    datos_en_json = data_response_5.json()
                    # Para guardar los datos en un archivo CSV
                    with open('climatologia.csv', 'w', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        # Escribir las variables
                        header = datos_en_json[0].keys()
                        csv_writer.writerow(header)
                        # Escrbir los valores (filas)
                        for entry in datos_en_json:
                            csv_writer.writerow(entry.values())
                else:
                    print(f"Error fetching the data: Response code {data_response_5.status_code}")
            else:
                print(f"Error fetching the data: Response code {url_datos_4.status_code}")
        else:
            print(f"Error fetching the data: Response code {response_climatologia_3.status_code}")
    else:
        print(f"Error fetching the data: Response code {data_response_2.status_code}")
else:
    print(f"Error fetching the data URL: Response code {response_1.status_code}")


#Encadena las peticiones a la API de la AEMET necesarias para descargar las temperaturas medias registradas
# por todas las estaciones de la AEMET durante todos los meses de agosto entre 2011 y 2020.
# Una vez obtenido todas las temperaturas medias de todos los meses de agosto, construye un array 
# con un elemento por año de la década, que equivalga a la media de temperatura nacional para ese mes de agosto.