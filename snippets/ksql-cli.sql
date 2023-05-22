-- Just to drop
DROP STREAM IF EXISTS geo_data;
-- list created streams
SHOW STREAMS;
-- Create a stream
-- Keys in the topic cant be reserved keywords like KEY or TIMESTAMP.
CREATE OR REPLACE STREAM geo_data (
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
-- To querie a stream
select ROWTIME, * from geo_data;
    