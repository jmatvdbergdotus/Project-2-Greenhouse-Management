from flask import Flask, render_template, g, jsonify
import sqlite3
import os

app = Flask(__name__)

# Database path
db_path = os.path.join(os.getcwd(), "raw_data.db")

# Connect to database
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

# Close connection after request
@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# Get table name safely
def get_table():
    db = get_db()
    result = db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ).fetchone()
    
    if result is None:
        return None
    
    return result[0]

# Route: Dashboard page
@app.route("/")
def greenhouse():
    db = get_db()
    table = get_table()

    if table is None:
        return "No table found in database"

    rows = db.execute(f"SELECT * FROM {table} LIMIT 50").fetchall()

    if not rows:
        return "No data found in table"

    columns = rows[0].keys()

    data = {col: [row[col] for row in rows] for col in columns}
    latest = rows[-1]

    return render_template(
        "greenhouse.html",
        data=data,
        columns=columns,
        latest=latest
    )

# Route: API for chart data
@app.route("/api/data")
def api_data():
    db = get_db()
    rows = db.execute(f"SELECT * FROM readings_with_status ORDER BY datetime DESC LIMIT 100").fetchall()
    return jsonify([dict(row) for row in rows])

@app.route("/api/historical")
def hist_data():
    db = get_db()
    rows = db.execute(f"SELECT * FROM readings_with_status ORDER BY datetime DESC LIMIT 100").fetchall()
    
    if not rows:
        return "No data found in table"

    columns = rows[0].keys()

    data = {col: [row[col] for row in rows] for col in columns}
    latest = rows[-1]
    
    return render_template(
        "table.html",
        data=data,
        columns=columns,
        latest=latest
    )

# Run app
if __name__ == "__main__":
    app.run(debug=True)