
from flask import Flask, render_template, request, redirect
import sqlite3
import random

app = Flask(__name__)

# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('quicktext.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the table if it doesn't exist
with get_db_connection() as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            text TEXT NOT NULL
        )
    ''')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_room():
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    text = request.form['text']
    with get_db_connection() as conn:
        conn.execute('INSERT INTO texts (code, text) VALUES (?, ?)', (code, text))
        conn.commit()
    return f'Room created with code: {code}'

@app.route('/enter', methods=['POST'])
def enter_code():
    code = request.form['code']
    with get_db_connection() as conn:
        text_entry = conn.execute('SELECT text FROM texts WHERE code = ?', (code,)).fetchone()
    if text_entry:
        return f'Text for code {code}: {text_entry["text"]}'
    else:
        return 'No entry found for that code.'

if __name__ == '__main__':
    app.run(debug=True)
