import logging
from bokeh.driving import count
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

from ksql_rest import get_ksql_data, KSQLDB

ksqldb_client = KSQLDB()
query = """SELECT * FROM geo_data_stream EMIT CHANGES;"""
data = get_ksql_data(ksqldb_client=ksqldb_client, query=query)

source = ColumnDataSource({'x': [], 'y': []})


@count()
def update(x):
	schema, list_data = next(data)
	logging.info(data)
	source.stream({'x': [list_data[0]], 'y': [list_data[-1]]}, rollover=50)


# Plot.
plot = figure(title='Total por fecha', height=100, x_axis_type="datetime")
plot.sizing_mode = 'scale_width'
plot.line('x', 'y', source=source)
plot.xaxis.axis_label = 'fecha'
plot.yaxis.axis_label = 'total'
plot.xaxis.major_label_orientation = 0.8  # radians

doc = curdoc()
doc.add_root(plot)
doc.add_periodic_callback(update, 500)
# bokeh serve  --log-level=debug --show visualization.py
