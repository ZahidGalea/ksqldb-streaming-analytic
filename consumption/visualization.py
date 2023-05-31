import os
from bokeh.driving import count
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

from ksql_rest import geo_data_stream_create, get_ksql_data, KSQLDB

ksqldb_client = KSQLDB()
domain = os.environ.get('KSQLDB_DOMAIN')
if domain:
	ksqldb_client.domain = domain
port = os.environ.get('KSQLDB_PORT')
if port:
	ksqldb_client.port = port

# Creates the stream if it doesn't exist.
reponse = geo_data_stream_create(ksqldb_client=ksqldb_client)

# Queries the data
query = """SELECT * FROM geo_data_stream EMIT CHANGES;"""
data = get_ksql_data(ksqldb_client=ksqldb_client, query=query)

total = ColumnDataSource({'x': [], 'y': []})
copper = ColumnDataSource({'x': [], 'y': []})
gold = ColumnDataSource({'x': [], 'y': []})


@count()
def update(x):
	schema, list_data = next(data)
	total.stream({'x': [list_data[0]], 'y': [list_data[-1]]}, rollover=100)
	copper.stream({'x': [list_data[0]], 'y': [list_data[-3]]}, rollover=100)
	gold.stream({'x': [list_data[0]], 'y': [list_data[-2]]}, rollover=100)


# Plot.
plot = figure(title='Total por fecha', height=100, x_axis_type="datetime")
plot.sizing_mode = 'scale_width'
plot.line('x', 'y', source=total, legend_label='total')
plot.line('x', 'y', source=copper, line_color='green', legend_label='copper')
plot.line('x', 'y', source=gold, line_color='orange', legend_label='gold')
plot.xaxis.axis_label = 'fecha'
plot.yaxis.axis_label = 'total'
# plot.xaxis.major_label_orientation = 0.8  # radians
plot.legend.title = 'Division'
plot.legend.border_line_width = 3
plot.legend.border_line_alpha = 0.5

doc = curdoc()
doc.add_root(plot)
doc.add_periodic_callback(update, 500)
# bokeh serve  --log-level=debug --show visualization.py
