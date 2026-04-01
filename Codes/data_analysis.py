import sqlite3
import pandas as pd

conn = sqlite3.connect("Data/raw_data.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS readings;")
cur.execute("""
    CREATE TABLE readings AS
    SELECT DATE || ' ' || TIME AS datetime, temp, hum, soil_moisture, par
        FROM MOCKDATA
""")

cur.execute("DROP TABLE IF EXISTS main.readings_with_status;")

cur.execute("""
    CREATE VIEW readings_with_status AS
SELECT
    r.*,

    -- TEMPERATURE
    CASE
        WHEN r.temp < 12.9 THEN 'below'
        WHEN r.temp > 31.5 THEN 'above'
        ELSE 'within'
    END AS temp_status,

    -- HUMIDITY
    CASE
        WHEN r.hum < 9.1 THEN 'below'
        WHEN r.hum > 83.2 THEN 'above'
        ELSE 'within'
    END AS hum_status,

    -- SOIL MOISTURE
    CASE
        WHEN r.soil_moisture < 16.5 THEN 'below'
        WHEN r.soil_moisture > 20.5 THEN 'above'
        ELSE 'within'
    END AS soil_status,

    -- PAR
    CASE
        WHEN r.par < 0.0 THEN 'below'
        WHEN r.par > 1926.0 THEN 'above'
        ELSE 'within'
    END AS par_status

FROM readings r;
""")