from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
from mysql.connector import Error
import random

app = Flask(__name__)

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='localguest001',  # Replace with your MySQL root password
            database='quicktext_db'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def generate_unique_code(connection):
    cursor = connection.cursor()
    while True:
        code = ''.join(random.choices('0123456789', k=6))
        cursor.execute("SELECT COUNT(*) FROM text_entries WHERE unique_code = %s", (code,))
        if cursor.fetchone()[0] == 0:
            return code

def save_entry(text, connection):
    code = generate_unique_code(connection)
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO text_entries (unique_code, text_entry) VALUES (%s, %s)", (code, text))
        connection.commit()
        return code
    except Error as e:
        print(f"Database error: {e}")
        return None

def get_text_by_code(code, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT text_entry FROM text_entries WHERE unique_code = %s", (code,))
    result = cursor.fetchone()
    return result[0] if result else None

@app.route('/submit-text', methods=['POST'])
def submit_text():
    data = request.json
    text = data.get('text')
    connection = create_connection()
    if connection:
        code = save_entry(text, connection)
        connection.close()
        if code:
            response = {'code': code}
            print(f"Submit response: {response}")  # Debug print
            return jsonify(response)
        return jsonify({'error': 'Error saving entry'}), 500
    return jsonify({'error': 'Database connection error'}), 500

@app.route('/retrieve-text', methods=['GET'])
def retrieve_text():
    code = request.args.get('code')
    connection = create_connection()
    if connection:
        text = get_text_by_code(code, connection)
        connection.close()
        if text:
            return jsonify({'text': text})
        return jsonify({'error': 'Code not found'}), 404
    return jsonify({'error': 'Database connection error'}), 500

@app.route('/generate-code', methods=['GET'])
def generate_code():
    connection = create_connection()
    if connection:
        code = generate_unique_code(connection)
        connection.close()
        return jsonify({'code': code})
    return jsonify({'error': 'Database connection error'}), 500

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
