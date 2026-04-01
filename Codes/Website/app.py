from flask import Flask, app
from flask import render_template, g
import sqlite3
import os

app = Flask(__name__)

db_path = os.path.join(os.getcwd(), "Data\\raw_data.db")

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

def get_table_and_columns():
    db = get_db()
    
    result = db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ).fetchone()
    
    if result is None:
        return None, None 
    
    table = result[0]
    
    cols = db.execute(f"PRAGMA table_info({table})").fetchall()
    columns = [c[1] for c in cols]
    
    return table, columns

@app.route("/")
def greenhouse():
    db = get_db()
    table, columns = get_table_and_columns()
    
    rows = db.execute(f"SELECT * FROM {table} LIMIT 50").fetchall()

    data = {col: [row[col] for row in rows] for col in columns}

    numeric_cols = []
    for col in columns:
        try:
            float(data[col][0])
            numeric_cols.append(col)
        except:
            pass

    latest = rows[-1] if rows else None

    return render_template("greenhouse.html",
        data=data, columns=columns,
        numeric_cols=numeric_cols,
        latest=latest)

if __name__ == "__main__":
    app.run(port=5000, debug=True)