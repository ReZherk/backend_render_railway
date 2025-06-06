from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_connection
import os

app = Flask(__name__)

# Permitir explícitamente el origen del frontend de desarrollo
CORS(app, origins=["http://localhost:5173"])

@app.route('/')
def home():
    return '¡Backend Flask desplegado correctamente!'

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return jsonify(success=True, message="Login exitoso")
    else:
        return jsonify(success=False, message="Credenciales inválidas"), 401

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
