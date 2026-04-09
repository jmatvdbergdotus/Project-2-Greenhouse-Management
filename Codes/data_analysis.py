import sqlite3
import pandas as pd

print("Connecting to database...")
conn = sqlite3.connect("Data/raw_data.db")
cur = conn.cursor()
print("Connected.\n")

# --- DROP + CREATE TABLE ---
print("Dropping existing table 'readings' (if exists)...")
cur.execute("DROP TABLE IF EXISTS readings;")
print("Table dropped (if it existed).")

print("Creating table 'readings' from MOCKDATA...")
cur.execute("""
    CREATE TABLE readings AS
    SELECT datetime(
        DATE || ' ' || 
        printf('%02d:%s', 
        CAST(substr(TIME, 1, instr(TIME, ':') - 1) AS INTEGER),
        substr(TIME, instr(TIME, ':') + 1)
    )
    ) AS datetime, temp, hum, soil_moisture, par
    FROM MOCKDATA
""")
print("Table 'readings' created.")

# --- ROW COUNT (TABLE) ---
cur.execute("SELECT COUNT(*) FROM readings ORDER BY datetime ASC;")
table_count = cur.fetchone()[0]

if table_count == 0:
    print("Warning: 'readings' table is empty!\n")
else:
    print(f"Table 'readings' contains {table_count} rows.\n")

# --- DROP VIEW ---
print("Dropping existing view 'readings_with_status' (if exists)...")
cur.execute("DROP VIEW IF EXISTS readings_with_status;")
print("View dropped (if it existed).")

# --- CREATE VIEW ---
print("Creating view 'readings_with_status' with status classifications...")
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
            WHEN r.par < 250.0 THEN 'below'
            WHEN r.par > 1400.0 THEN 'above'
            ELSE 'within'
        END AS par_status

    FROM readings r;
""")
print("View 'readings_with_status' created.")

# --- ROW COUNT (VIEW) ---
cur.execute("SELECT COUNT(*) FROM readings_with_status ORDER BY datetime ASC;")
view_count = cur.fetchone()[0]

if view_count == 0:
    print("Warning: 'readings_with_status' view returns no rows!\n")
else:
    print(f"View 'readings_with_status' contains {view_count} rows.\n")

# --- FINALIZE ---
conn.commit()
print("Changes committed to database.")

conn.close()
print("Connection closed.")

print("\nAll queries executed successfully!")