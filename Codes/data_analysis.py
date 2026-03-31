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

cur.execute("""
    ALTER TABLE readings ADD COLUMN temp001 INT;
""")

cur.execute("""
    UPDATE readings 
    SET temp001 = 1
    WHERE temp >= 31.5
""")
