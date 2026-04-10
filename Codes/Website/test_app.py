from app import app


# Test 1: Flask App is running and home page loads
def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

# Test 2: API Returns data
def test_api_data():
    client = app.test_client()
    response = client.get("/api/data")

    assert response.status_code == 200
    assert response.is_json

# Test 3: Data not Empty
def test_data_not_empty():
    client = app.test_client()
    response = client.get("/api/data")

    data = response.get_json()
    assert len(data) > 0

# Test 4: Check for required fields
def test_data_fields():
    client = app.test_client()
    response = client.get("/api/data")

    data = response.get_json()

    sample = data[0]

    assert "temp" in sample
    assert "hum" in sample
    assert "soil_moisture" in sample
    assert "par" in sample

# Test 5: Database Connection
import sqlite3

def test_database_connection():
    conn = sqlite3.connect("raw_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    assert len(tables) > 0