# Importar bibliotecas necesarias

from flask import Flask, jsonify  # Flask es el framework web, jsonify convierte objetos Python a JSON
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy es un ORM para trabajar con bases de datos
from flask_marshmallow import Marshmallow  # Marshmallow es para serialización/deserialización de objetos
from flask_jwt_extended import JWTManager  # JWTManager maneja la autenticación con tokens JWT
import json  # Para leer archivos JSON
import os  # Para operaciones con el sistema de archivos

# Inicializar la aplicación Flask
app = Flask(__name__)

# Cargar configuración desde el archivo JSON
# os.path.dirname(__file__) obtiene el directorio donde está este archivo
# os.path.join combina rutas de manera compatible con diferentes sistemas operativos
ruta_config = os.path.join(os.path.dirname(__file__), 'configuracion/config.json')
with open(ruta_config) as archivo_config:
    # Cargar los datos del archivo JSON en un diccionario de Python
    datos_config = json.load(archivo_config)

# Obtener el proveedor de base de datos seleccionado
# .get() permite obtener valores de un diccionario con un valor predeterminado si la clave no existe
proveedor_bd = datos_config.get("DatabaseProvider")
cadena_conexion = datos_config.get("ConnectionStrings", {}).get(proveedor_bd)

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = cadena_conexion  # URI de conexión a la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar seguimiento de modificaciones para mejorar rendimiento

# Configurar JWT (JSON Web Tokens) para autenticación
app.config['JWT_SECRET_KEY'] = datos_config.get("Jwt", {}).get("Key")  # Clave secreta para firmar tokens
app.config['JWT_ISSUER'] = datos_config.get("Jwt", {}).get("Issuer")  # Emisor de los tokens
app.config['JWT_AUDIENCE'] = datos_config.get("Jwt", {}).get("Audience")  # Audiencia de los tokens

# Inicializar extensiones
db = SQLAlchemy(app)  # Inicializar SQLAlchemy con la app
ma = Marshmallow(app)  # Inicializar Marshmallow con la app
jwt = JWTManager(app)  # Inicializar JWT con la app

# Definir una ruta básica para verificar que la API funciona
@app.route('/')  # Decorador que indica que esta función responde a la ruta '/'
def inicio():
    # Devolver un objeto JSON con un mensaje
    return jsonify({"mensaje": "API Flask funcionando correctamente"})


# Agregar esta nueva ruta después de la ruta principal (raiz)
@app.route('/weatherforecast')
def pronostico_clima():
    """
    Devolver datos ficticios de pronóstico del clima como prueba
    Similar al endpoint por defecto en una API de C#
    """
    datos_clima = [
        {
            "date": "2025-02-27",
            "temperatureC": 12,
            "summary": "Chilly",
            "temperatureF": 53
        },
        {
            "date": "2025-02-28",
            "temperatureC": 4,
            "summary": "Cool",
            "temperatureF": 39
        },
        {
            "date": "2025-03-01",
            "temperatureC": 13,
            "summary": "Mild",
            "temperatureF": 55
        },
        {
            "date": "2025-03-02",
            "temperatureC": -8,
            "summary": "Mild",
            "temperatureF": 18
        },
        {
            "date": "2025-03-03",
            "temperatureC": 44,
            "summary": "Hot",
            "temperatureF": 111
        }
    ]
    return jsonify(datos_clima)


# Punto de entrada para ejecutar la aplicación
if __name__ == '__main__':
    # Iniciar el servidor de desarrollo de Flask
    # debug=True habilita el modo de desarrollo (mensajes de error detallados, recarga automática)
    # Para producción, cambiar a debug=False
    # El puerto predeterminado es 5000, pero puede cambiarse
    app.run(debug=True, port=5000)
    
    # Para cambiar el puerto, modificar el parámetro port:
    # app.run(debug=True, port=8080)
    
    # Para producción, usar:
    # app.run(debug=False, host='0.0.0.0', port=5000)
