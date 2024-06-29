from flask import Flask, render_template, request, jsonify
import sqlite3
import random

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('quicktext.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create table if it doesn't exist
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            text TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    text = request.json.get('text')
    code = ''.join(random.choices('0123456789', k=6))
    
    conn = get_db_connection()
    conn.execute('INSERT INTO texts (code, text) VALUES (?, ?)', (code, text))
    conn.commit()
    conn.close()
    
    return jsonify({'code': code})

@app.route('/fetch', methods=['POST'])
def fetch():
    code = request.json.get('code')
    
    conn = get_db_connection()
    text_data = conn.execute('SELECT text FROM texts WHERE code = ?', (code,)).fetchone()
    conn.close()
    
    if text_data:
        return jsonify({'text': text_data['text']})
    else:
        return jsonify({'error': 'Invalid code'})

if __name__ == '__main__':
    app.run(debug=True)
