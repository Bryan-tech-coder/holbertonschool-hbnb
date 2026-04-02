# delete_user.py
from app import create_app, db
from app.persistence.repository import UserRepository
from config import Config

app = create_app(Config)
repo = UserRepository()

email = "admin@example.com"

with app.app_context():
    user = repo.get_user_by_email(email)
    if user:
        db.session.delete(user)
        db.session.commit()
        print(f"Usuario {email} eliminado.")
    else:
        print(f"Usuario {email} no existe.")
