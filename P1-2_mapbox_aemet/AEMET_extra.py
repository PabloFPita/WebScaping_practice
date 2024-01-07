import requests
import csv
import sys

def get_api_key():
    if len(sys.argv) < 2:
        print("Please provide the API key as the first argument when executing the script.")
        sys.exit(1)
    return sys.argv[1]

def get_all_stations(api_key):
    url_all_stations = f"https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"
    response_1 = requests.get(url_all_stations, params={'api_key': api_key})
    
    if response_1.status_code == 200:
        data_response_2 = requests.get(response_1.json()["datos"])
        if data_response_2.status_code == 200:
            return data_response_2.json()
        else:
            print(f"Error fetching the data: Response code {data_response_2.status_code}")
            sys.exit(1)
    else:
        print(f"Error fetching the data URL: Response code {response_1.status_code}")
        sys.exit(1)

def get_indicativo(all_stations, estacion_buscada):
    return next((entry["indicativo"] for entry in all_stations if entry["nombre"] == estacion_buscada), None)

def get_climatologia_url(indicativo, fecha_ini, fecha_fin):
    return f"https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{fecha_ini}/fechafin/{fecha_fin}/estacion/{indicativo}"

def get_climatologia_data(api_key, climatologia_url):
    try:
        response_climatologia_3 = requests.get(climatologia_url, params={'api_key': api_key})
        
        if response_climatologia_3.status_code == 200:
            url_datos_4 = requests.get(response_climatologia_3.url)
            
            if url_datos_4.status_code == 200:
                print(url_datos_4.json())
                
                return url_datos_4.json()['datos']
            else:
                print(f"Error fetching the data: Response code {url_datos_4.status_code}")
                sys.exit(1)
        else:
            print(f"Error fetching the data: Response code {response_climatologia_3.status_code}")
            sys.exit(1)
    except KeyError as e:
        print(f"KeyError: {e}. Unable to find 'datos' key in the response JSON.")
        pass

def download_and_save_data(data_url, station_name):
    data_response_5 = requests.get(data_url)
    
    if data_response_5.status_code == 200:
        datos_en_json = data_response_5.json()
        with open('climatologia_agostos.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            # Write header if file is empty
            if csvfile.tell() == 0:
                header = list(datos_en_json[0].keys()) + ["NombreEstacion"]
                csv_writer.writerow(header)
            
            for entry in datos_en_json:
                csv_writer.writerow(list(entry.values()) + [station_name])
    else:
        print(f"Error fetching the data: Response code {data_response_5.status_code}")
        sys.exit(1)

def main():
    api_key = get_api_key()
    all_stations = get_all_stations(api_key)
    print(f"Found {len(all_stations)} stations")

    for station in all_stations:
        indicativo = station["indicativo"]
        print(f"Processing data for station {station['nombre']} (Indicativo: {indicativo})")

        climatologia_url = get_climatologia_url(indicativo, "2016-08-01T00:00:00UTC", "2020-08-31T23:59:59UTC")
        data_url = get_climatologia_data(api_key, climatologia_url)
        
        download_and_save_data(data_url, station['nombre'])

if __name__ == "__main__":
    main()




#Encadena las peticiones a la API de la AEMET necesarias para descargar las temperaturas medias registradas
# por todas las estaciones de la AEMET durante todos los meses de agosto entre 2011 y 2020.
    

    
# Una vez obtenido todas las temperaturas medias de todos los meses de agosto, construye un array 
# con un elemento por año de la década, que equivalga a la media de temperatura nacional para ese mes de agosto.