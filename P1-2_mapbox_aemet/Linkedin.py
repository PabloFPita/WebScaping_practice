# Importar librería requests
import requests

# URL de la API de AEMET
url_all_stations = f"https://www.linkedin.com/in/pablofernandezpita/"

# Llamar a la API de AEMET para obtener los datos con la clave de API
response_1 = requests.get(url_all_stations)

print(response_1.status_code)