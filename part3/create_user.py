# create_user.py
from datetime import datetime, timezone
from app import create_app, db
from app.models.user import User
from app.persistence.repository import UserRepository
from config import Config
from app.models.user import bcrypt

# Crear la app
app = create_app(Config)

# Definir usuario que quieres crear
email = "admin@example.com"
password_plain = "supersecretpassword"

# Hashear la contraseña
hashed_pw = bcrypt.generate_password_hash(password_plain).decode("utf-8")
# Crear instancia del repositorio
repo = UserRepository()

# Todo lo que toca la DB debe ir dentro del app_context
with app.app_context():
    # Crear todas las tablas si no existen
    db.create_all()

    # Verificar si el usuario ya existe
    existing_user = repo.get_user_by_email(email)
    if existing_user:
        print(f"Usuario con email {email} ya existe!")
    else:
        # Crear el usuario
        user = User(
            email=email,
            password=hashed_pw,
            first_name="Admin",
            last_name="User",
            is_admin=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        # Guardar en la DB
        repo.add(user)
        print(f"Usuario {email} creado correctamente!")
