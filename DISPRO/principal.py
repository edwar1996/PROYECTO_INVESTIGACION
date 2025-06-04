from flask import Flask
from app import auth  # Importar el Blueprint de autenticación (antes app.py)
from app2 import users  # Importar el Blueprint de usuarios (antes app2.py)

# Crear la aplicación Flask
app = Flask(__name__)

# Registrar los blueprints
app.register_blueprint(auth, url_prefix='/auth')  # El blueprint auth se sirve en /auth
app.register_blueprint(users, url_prefix='/users')  # El blueprint users se sirve en /users

# Configuración adicional (como claves, bases de datos, etc.)
# app.config['SECRET_KEY'] = 'mi_clave_secreta'  # Si se necesita una clave secreta, descomentar esta línea

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)  # Ejecutar en modo debug para desarrollo
