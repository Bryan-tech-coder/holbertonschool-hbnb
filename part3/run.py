import os
from app import create_app
from config import Config
from flask import send_from_directory

app = create_app(Config)

# 🔥 ruta absoluta correcta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PART4_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'part4'))

print("📁 PART4_DIR:", PART4_DIR)  # DEBUG

@app.route('/')
def serve_login():
    return send_from_directory(PART4_DIR, 'login.html')

@app.route('/<path:filename>')
def serve_frontend(filename):
    return send_from_directory(PART4_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
