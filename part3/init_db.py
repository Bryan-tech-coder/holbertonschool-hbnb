# init_db.py
from app import create_app, db
from config import Config

app = create_app(Config)

with app.app_context():
    db.create_all()
    print("Base de datos inicializada")
