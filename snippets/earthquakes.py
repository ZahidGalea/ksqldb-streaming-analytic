import requests

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Parámetros de la consulta
payload = {
	"format": "geojson",
	"starttime": "2023-04-01",
	"endtime": "2023-04-06",
	"minmagnitude": 6
}

response = requests.get(url, params=payload)

if response.status_code == 200:
	# La solicitud fue exitosa
	print(response.json())
# Manejar la respuesta de la API
else:
	# La solicitud falló
	print("Error al hacer la consulta: ", response.status_code)
