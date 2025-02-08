import sqlite3

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS temperature (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS weight (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            weight REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_temperature_to_db(temperature_value):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO temperature (temperature) VALUES (?)', (temperature_value,))
    conn.commit()
    conn.close()

def save_weight_to_db(weight_value):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO weight (weight) VALUES (?)', (weight_value,))
    conn.commit()
    conn.close()

def get_temperature_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM temperature ORDER BY timestamp DESC')
    data = c.fetchall()
    conn.close()
    return data

def get_weight_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM weight ORDER BY timestamp DESC')
    data = c.fetchall()
    conn.close()
    return data
def get_latest_temperature():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT temperature FROM temperature ORDER BY timestamp DESC LIMIT 1')
    data = c.fetchone()
    conn.close()
    return data[0] if data else "N/A"  # Vrátí hodnotu nebo "N/A"

def get_latest_weight():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT weight FROM weight ORDER BY timestamp DESC LIMIT 1')
    data = c.fetchone()
    conn.close()
    return data[0] if data else "N/A"  # Vrátí hodnotu nebo "N/A"


def average_temperature():
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT temperature FROM temperature')
        rows = cursor.fetchall()

        if rows:
            values = [float(row[0]) for row in rows]
            average = sum(values) / len(values)
            print(f'Průměr teplotních záznamů je: {average:.2f}')
            return average
        else:
            print('V databázi nejsou žádné záznamy.')
            return None

    except sqlite3.Error as e:
        print(f'Došlo k chybě při práci s databází: {e}')
        return None

    finally:
        if conn:
            conn.close()