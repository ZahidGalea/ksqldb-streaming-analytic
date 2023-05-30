import json
import logging
import os
import requests
import time

logging.basicConfig(level='INFO')
log = logging.getLogger(__name__)


class KSQLDB:
	_domain: str = "localhost"
	_port: str = '8088'
	headers: dict

	def __init__(self):
		self.headers = {
			"Accept": "application/vnd.ksql.v1+json",
			"Content-Type": "application/vnd.ksql.v1+json"
		}

	@property
	def domain(self):
		return self._domain

	@domain.setter
	def domain(self, value):
		self._domain = value

	@property
	def port(self):
		return self._port

	@port.setter
	def port(self, value):
		self._port = value

	@property
	def query_endpoint_url(self) -> str:
		"""
		Builds the ksql url
		:return:  
		"""
		return f"http://{self.domain}:{self.port}/query"

	@property
	def ksql_endpoint_url(self) -> str:
		"""
		Builds the ksql url
		:return:  
		"""
		return f"http://{self.domain}:{self.port}/ksql"

	@property
	def ksql_queries_url(self) -> str:
		"""
		Builds the ksql url
		:return:  
		"""
		return f"http://{self.domain}:{self.port}/query-stream"

	def list_streams(self):
		data = {
			"ksql": "LIST STREAMS;",
			"streamsProperties": {}  # https://docs.ksqldb.io/en/latest/reference/server-configuration/
		}

		return requests.post(self.ksql_endpoint_url, headers=self.headers, data=json.dumps(data))

	def execute_ksql(self, ksql: str, stream_property: dict = {}):
		data = {
			"ksql": ksql.replace("\n", "").replace("\t", ''),
			"streamsProperties": stream_property  # https://docs.ksqldb.io/en/latest/reference/server-configuration/
		}
		return requests.post(self.ksql_endpoint_url, headers=self.headers, data=json.dumps(data))

	def execute_ksql_stream_querie(self, ksql: str, stream_property: dict = {}):
		data = {
			"sql": ksql.replace("\n", "").replace("\t", ''),
			"properties": stream_property  # https://docs.ksqldb.io/en/latest/reference/server-configuration/
		}
		return requests.post(self.ksql_queries_url, headers=self.headers, data=json.dumps(data), stream=True)


def validate_execution(response):
	if not response.ok:
		if response.json()[0]['commandStatus']['status'] != 'SUCCESS':
			log.error(f'Something failed {response.json()}')
			return False
	return True


def clean_data(data: list):
	from datetime import datetime
	data[0] = datetime.fromtimestamp(int(data[0]) / 1000)
	return data


def get_ksql_data(ksqldb_client, query: str) -> (list, list):
	schema_names = []
	response = ksqldb_client.execute_ksql_stream_querie(ksql=query)
	try:
		for line in response.iter_lines():
			time.sleep(1)
			# Filtra las líneas de keep-alive (nuevas líneas en la respuesta HTTP)
			if line:
				line_cleaned = line.decode("utf-8")[
							   :-1]  # Borra el ultimo caracter ya que es una "," de separacion de filas.

				# Si es la primera línea, crea la clase de datos
				if 'header' in line_cleaned:
					parsed_line = json.loads(line_cleaned.replace('[', '').replace(']', ''))
					schema_names = parsed_line['header']['schema'].split(',')
					schema_names = [name.replace('`', '').strip().split(" ") for name in
									schema_names]  # Limpia los nombres de columnas y separa del tipo de dato.

				# Si no es la primera línea, crea una instancia de la clase de datos
				elif 'row' in line_cleaned:
					parsed_line = json.loads(line_cleaned)
					data_list = parsed_line['row']['columns']
					data_list = clean_data(data_list)
					yield schema_names, data_list
	except KeyboardInterrupt:
		print("Deteniendo...")


def geo_data_stream(ksqldb_client: KSQLDB):
	streams = ksqldb_client.list_streams()
	log.info(streams.json())
	# Crear el stream
	stream_creation = """
	CREATE OR REPLACE STREAM geo_data_stream (
			EVENT_TIMESTAMP VARCHAR,
			ID VARCHAR,
			SENSOR_ID INT,
			COPPER DOUBLE,
			GOLD DOUBLE,
			TOTAL DOUBLE
		)
		  WITH (kafka_topic='geo_data',
			VALUE_FORMAT='JSON');
	"""
	response = ksqldb_client.execute_ksql(ksql=stream_creation)
	if not validate_execution(response):
		raise Exception(f'Execution failed')

	# Obtener datos del stream.
	query = """SELECT * FROM geo_data_stream EMIT CHANGES;"""
	for schema, lista in get_ksql_data(ksqldb_client=ksqldb_client, query=query):
		print(schema)
		print(lista)


if __name__ == '__main__':

	ksqldb_client = KSQLDB()
	domain = os.environ.get('KSQLDB_DOMAIN')
	if domain:
		ksqldb_client.domain = domain
	port = os.environ.get('KSQLDB_PORT')
	if port:
		ksqldb_client.port = port
	geo_data_stream(ksqldb_client)
