# create_user.py
from app import create_app
from app.persistence.repository import UserRepository
from app.models.user import User, bcrypt
from config import Config

# Crear app y repositorio
app = create_app(Config)
repo = UserRepository()

# Datos del usuario
email = "bryancito@example.com"
password = "123456"
hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

# Crear usuario en la base de datos
user = User(email=email, password=hashed_pw, is_admin=False)

# Guardar usuario usando tu repo
with app.app_context():
    repo.add_user(user)

print(f"Usuario {email} creado correctamente")
