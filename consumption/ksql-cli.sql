-- Just to drop
DROP
STREAM IF EXISTS geo_data_stream;
-- list created streams
SHOW
STREAMS;
DESCRIBE geo_data_stream EXTENDED;
-- Create a stream
-- Keys in the topic cant be reserved keywords like KEY or TIMESTAMP.
CREATE
OR REPLACE STREAM geo_data_stream (
    EVENT_TIMESTAMP VARCHAR,
    ID VARCHAR,
    SENSOR_ID INT,
    COPPER DOUBLE,
    GOLD DOUBLE,
    TOTAL DOUBLE
)
  WITH (kafka_topic='geo_data',
    VALUE_FORMAT='JSON',
    timestamp='EVENT_TIMESTAMP',
    timestamp_format='yyyy-MM-dd HH-mm-ss');
    

CREATE
OR REPLACE STREAM geo_data_stream (
    EVENT_TIMESTAMP VARCHAR,
    ID VARCHAR,
    SENSOR_ID INT,
    COPPER DOUBLE,
    GOLD DOUBLE,
    TOTAL DOUBLE
)
  WITH (kafka_topic='geo_data',
    VALUE_FORMAT='JSON');
-- Some queries
select ROWTIME, *
from geo_data_stream;
---
-- Push queries enable you to subscribe to changes, which enable reacting to new information in real-time. They’re a good fit for asynchronous application flows
SELECT *
FROM geo_data_stream
WHERE gold > 40 EMIT CHANGES;
--
SELECT sensor_id, SUM(copper), SUM(gold)
FROM geo_data_stream
GROUP BY sensor_id;
--
SELECT CAST(PARSE_TIMESTAMP(EVENT_TIMESTAMP, 'yyyy-MM-dd HH:mm:ss') AS DATE) AS EVENT_TIMESTAMP,
       TIMESTAMPTOSTRING(windowstart, 'yyyy-MM-dd HH:mm:ss') AS WINDOW_START,
       TIMESTAMPTOSTRING(windowend, 'yyyy-MM-dd HH:mm:ss')   AS WINDOW_END,
       AVG(copper)                                           AS MEDIA_COPPER,
       AVG(gold)                                             AS MEDIA_GOLD
FROM geo_data_stream WINDOW TUMBLING  (SIZE 10 SECONDS)
GROUP BY EVENT_TIMESTAMP, 'yyyy-MM-dd HH:mm:ss'), 'yyyy-MM-dd')
    EMIT CHANGES;
---
SELECT FORMAT_TIMESTAMP(PARSE_TIMESTAMP(EVENT_TIMESTAMP, 'yyyy-MM-dd HH-mm-ss'), 'yyyy-MM-dd'),
       TIMESTAMPTOSTRING(windowstart, 'yyyy-MM-dd HH:mm:ss') AS WINDOW_START,
       TIMESTAMPTOSTRING(windowend, 'yyyy-MM-dd HH:mm:ss')   AS WINDOW_END,
       AVG(copper)                                           AS MEDIA_COPPER,
       AVG(gold)                                             AS MEDIA_GOLD
FROM geo_data_stream WINDOW TUMBLING  (SIZE 31 SECONDS)
WHERE CAST (PARSE_TIMESTAMP(EVENT_TIMESTAMP, 'yyyy-MM-dd HH-mm-ss') AS DATE) >= '2023-05-01'

GROUP BY FORMAT_TIMESTAMP(PARSE_TIMESTAMP(EVENT_TIMESTAMP, 'yyyy-MM-dd HH-mm-ss'), 'yyyy-MM-dd')
    EMIT CHANGES;



SELECT 
    TIMESTAMPTOSTRING(WINDOWSTART, 'yyyy-MM-dd HH:mm:ss') AS start_timestamp,
    sensor_id,
    SUM(copper) AS sum_copper,
    SUM(gold) AS sum_gold,
    COUNT(*) as q_de_registros
FROM geo_data_stream
WINDOW TUMBLING (SIZE 31 SECONDS)
GROUP BY sensor_id
EMIT CHANGES;
