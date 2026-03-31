from app import create_app
from config import Config
from flask import send_from_directory

# Crear la app usando tu factory
app = create_app(Config)

# Servir login.html desde part4
@app.route('/')
def serve_login():
    return send_from_directory('../part4', 'login.html')

# Servir otros archivos de frontend
@app.route('/<path:filename>')
def serve_frontend(filename):
    return send_from_directory('../part4', filename)

if __name__ == "__main__":
    # Correr Flask en modo debug
    app.run(debug=True)
