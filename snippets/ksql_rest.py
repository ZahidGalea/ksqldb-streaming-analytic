import json
import os

import requests


class KSQLDB:
	_domain: str = "localhost"
	_port: str = '8088'
	headers: dict

	def __init__(self):
		self.headers = {
			"Accept": "application/vnd.ksql.v1+json",
			"Content-Type": "application/json"
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

	def list_streams(self):
		data = {
			"ksql": "LIST STREAMS;",
			"streamsProperties": {}
		}

		return requests.post(self.ksql_endpoint_url, headers=self.headers, data=json.dumps(data))

	def execute_ksql(self, ksql: str, stream_property: dict):
		data = {
			"ksql": ksql,
			"streamsProperties": stream_property
		}
		return requests.post(self.ksql_endpoint_url, headers=self.headers, data=json.dumps(data))


def main(ksqldb_client):
	streams = ksqldb_client.list_streams()
	print(streams.json())
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
	ksqldb_client.execute_ksql()


if __name__ == '__main__':
	ksqldb_client = KSQLDB()
	domain = os.environ.get('KSQLDB_DOMAIN')
	if domain:
		ksqldb_client.domain = domain
	port = os.environ.get('KSQLDB_PORT')
	if port:
		ksqldb_client.port = port

	main(ksqldb_client=ksqldb_client)
