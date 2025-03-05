# app.py - Punto de entrada principal para la API Flask
# Este archivo equivale a Program.cs en una API de C#

# Importación de bibliotecas necesarias (equivalentes a los "using" en C#)
from flask import Flask, jsonify, request  # Flask es el framework web principal
from flask_sqlalchemy import SQLAlchemy  # ORM para trabajar con bases de datos
from flask_marshmallow import Marshmallow  # Para serialización/deserialización de objetos
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity  # Para autenticación con JWT
from flask_cors import CORS  # Para habilitar CORS (permite peticiones desde diferentes dominios)
from flask_session import Session  # Para manejo de sesiones (equivalente a builder.Services.AddSession)
import json  # Para leer archivos JSON de configuración
import os  # Para operaciones con rutas de archivos
import datetime  # Para manejo de fechas y tiempos (equivalente a System en C#)
from flasgger import Swagger  # Para documentación de API (equivalente a Swagger en C#)
import pandas as pd  # Para manejar datos tabulares (equivalente a DataTable en C#)
import bcrypt  # Para hashear contraseñas (equivalente a BCrypt.Net en C#)
import traceback  # Para depuración de errores
import pyodbc  # Para conexiones a SQL Server (equivalente a Microsoft.Data.SqlClient)

# Inicializar la aplicación Flask (equivalente a var builder = WebApplication.CreateBuilder(args))
# Esta es la línea más importante: crea la instancia principal de la aplicación Flask
app = Flask(__name__)

# Cargar configuración desde archivo JSON (equivalente a appsettings.json)
# Construimos la ruta al archivo de configuración y lo cargamos
ruta_config = os.path.join(os.path.dirname(__file__), 'configuracion', 'config.json')
with open(ruta_config) as archivo_config:
    datos_config = json.load(archivo_config)

# Configuración de la base de datos
# Obtenemos el proveedor seleccionado en la configuración
proveedor_bd = datos_config.get("DatabaseProvider")
cadena_conexion = datos_config.get("ConnectionStrings", {}).get(proveedor_bd)

# Configurar la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = cadena_conexion  # Cadena de conexión
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar seguimiento para mejor rendimiento

# Configuración de JWT (equivalente a configuración JWT en C#)
app.config['JWT_SECRET_KEY'] = datos_config.get("Jwt", {}).get("Key")  # Clave secreta para tokens
app.config['JWT_ISSUER'] = datos_config.get("Jwt", {}).get("Issuer")  # Emisor de tokens
app.config['JWT_AUDIENCE'] = datos_config.get("Jwt", {}).get("Audience")  # Audiencia de tokens

# Configuración de sesiones (equivalente a builder.Services.AddSession)
app.config['SECRET_KEY'] = datos_config.get("Jwt", {}).get("Key")  # Clave para sesiones
app.config['SESSION_TYPE'] = 'filesystem'  # Almacenar sesiones en archivos
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)  # Tiempo de vida de 30 minutos
app.config['SESSION_USE_SIGNER'] = True  # Firmar cookies para seguridad
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Cookie solo accesible por HTTP

# Inicializar extensiones/servicios (equivalente a builder.Services.Add...)
db = SQLAlchemy(app)  # Inicializar ORM para base de datos
ma = Marshmallow(app)  # Inicializar serializador
jwt = JWTManager(app)  # Inicializar JWT para autenticación
sess = Session(app)  # Inicializar manejo de sesiones

# Configurar CORS para permitir solicitudes desde cualquier origen
# Equivalente a builder.Services.AddCors con AllowAnyOrigin/Method/Header
CORS(app, resources={r"/*": {"origins": "*"}})

# Configurar Swagger para documentación de API (equivalente a builder.Services.AddSwaggerGen)
swagger_config = {
    "title": "API Genérica Flask",
    "version": "1.0.0",
    "description": "API de prueba con Flask y Swagger",
    "termsOfService": "",
    "contact": {
        "name": "Soporte API",
        "email": "soporte@miapi.com",
        "url": "https://miapi.com/contacto",
    },
}
swagger = Swagger(app, template=swagger_config)

# Importar servicios propios (equivalente a using csharpapigenerica.Services)
# Estos archivos deben existir en las carpetas respectivas
from servicios.control_conexion import ControlConexion
from servicios.token_service import TokenService

# Inicializar servicios (equivalente a builder.Services.AddSingleton)
# En Flask se usan variables globales en lugar de inyección de dependencias
control_conexion = ControlConexion()
token_service = TokenService()

# Manejadores de errores (middleware de error)
@app.errorhandler(404)
def recurso_no_encontrado(error):
    """Manejador para errores 404 (Not Found)"""
    return jsonify({"error": "Recurso no encontrado"}), 404

@app.errorhandler(500)
def error_servidor(error):
    """Manejador para errores 500 (Server Error)"""
    return jsonify({"error": "Error interno del servidor"}), 500

#######################################################################
# RUTAS BÁSICAS DE LA API (EQUIVALENTE A CONTROLLERS EN C#)
#######################################################################

# Definir rutas básicas (equivalente a los controladores en C#)
# El decorador @app.route define qué URL atenderá esta función
@app.route('/')  # Ruta principal de la API (raíz)
def inicio():
    """
    Endpoint de la raíz de la API.
    Muestra un mensaje de bienvenida con información básica sobre la API.
    
    Returns:
        JSON: Mensaje de bienvenida con información de la API.
    """
    # Creamos un diccionario con los datos que queremos devolver
    mensaje = {
        "mensaje": "Bienvenido a la API Genérica en Flask!",
        "documentacion": "Para más detalles, visita /swagger",
        "fecha_servidor": datetime.datetime.utcnow().isoformat()
    }
    
    # Convertimos el diccionario a formato JSON y lo devolvemos
    return jsonify(mensaje)

@app.route('/weatherforecast')  # Ruta de ejemplo con datos de clima
def pronostico_clima():
    """
    Devuelve datos ficticios de pronóstico del clima como prueba
    Similar al endpoint por defecto en una API de C#
    ---
    responses:
      200:
        description: Pronóstico del clima para los próximos días
    """
    # Datos de ejemplo del pronóstico del clima
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
    # Convertimos la lista a formato JSON y la devolvemos
    return jsonify(datos_clima)
#######################################################################
# IMPLEMENTACIÓN DE ENTIDADESCONTROLLER
#######################################################################

# Función auxiliar para convertir elementos JSON a tipos de datos Python
def convertir_json_element(elemento):
    """
    Convierte un elemento JSON a su tipo de dato correspondiente en Python.
    Es equivalente al método ConvertirJsonElement en C#.
    
    Args:
        elemento: Valor JSON a convertir.
        
    Returns:
        object: Valor convertido a su tipo correspondiente.
    """
    # Si es None, devolvemos None
    if elemento is None:
        return None
    
    # Si es una cadena, intentamos convertir a fecha
    if isinstance(elemento, str):
        try:
            # Intentamos interpretar la cadena como fecha ISO
            return datetime.datetime.fromisoformat(elemento.replace('Z', '+00:00'))
        except ValueError:
            # Si no es una fecha válida, devolvemos la cadena original
            return elemento
    
    # Si es un número, lo devolvemos sin cambios
    if isinstance(elemento, (int, float)):
        return elemento
    
    # Si es un booleano, lo devolvemos sin cambios
    if isinstance(elemento, bool):
        return elemento
    
    # Si es un objeto o array JSON, lo convertimos a una cadena JSON
    if isinstance(elemento, (dict, list)):
        return json.dumps(elemento)
    
    # Por defecto, devolvemos el elemento sin cambios
    return elemento

# Función para obtener el prefijo de parámetro según el proveedor de base de datos
def obtener_prefijo_parametro(proveedor):
    """
    Obtiene el prefijo adecuado para los parámetros SQL según el proveedor.
    Es equivalente al método ObtenerPrefijoParametro en C#.
    
    Args:
        proveedor (str): Nombre del proveedor de base de datos.
        
    Returns:
        str: Prefijo para los parámetros.
    """
    # Para SQL Server y LocalDB es "@", podríamos añadir más condiciones para otros proveedores
    return "@"

# Rutas de EntidadesController

# Listar todos los registros de una tabla
@app.route('/api/<string:nombre_proyecto>/<string:nombre_tabla>', methods=['GET'])
def listar(nombre_proyecto, nombre_tabla):
    """
    Obtiene todos los registros de una tabla específica en la base de datos.
    Es equivalente al método Listar() en EntidadesController.cs.
    
    Args:
        nombre_proyecto (str): Nombre del proyecto al que pertenece la tabla.
        nombre_tabla (str): Nombre de la tabla a consultar.
        
    Returns:
        JSON: Lista de registros en formato JSON si la consulta es exitosa, o un código de error en caso de fallo.
    """
    # Verificar si el nombre de la tabla está vacío
    if not nombre_tabla or nombre_tabla.strip() == "":
        return jsonify({"error": "El nombre de la tabla no puede estar vacío"}), 400
    
    try:
        # Lista para almacenar las filas obtenidas
        lista_filas = []
        
        # Consulta SQL simple para obtener todos los registros
        comando_sql = f"SELECT * FROM {nombre_tabla}"
        
        # Abrir conexión, ejecutar consulta y cerrar conexión
        control_conexion.abrir_bd()
        tabla_resultados = control_conexion.ejecutar_consulta_sql(comando_sql)
        control_conexion.cerrar_bd()
        
        # Convertir DataFrame a lista de diccionarios para devolver como JSON
        if not tabla_resultados.empty:
            lista_filas = tabla_resultados.to_dict('records')
            
            # Convertir valores especiales como timestamps y NaN
            for fila in lista_filas:
                for clave, valor in fila.items():
                    # Si es NaN (Not a Number), convertir a None
                    if pd.isna(valor):
                        fila[clave] = None
                    # Si es un timestamp, convertir a cadena ISO
                    elif isinstance(valor, pd.Timestamp):
                        fila[clave] = valor.isoformat()
        
        # Devolver lista de filas en formato JSON
        return jsonify(lista_filas)
        
    except pyodbc.Error as ex:
        # Mapear códigos de error SQL a códigos HTTP apropiados
        codigo_error = 500
        if hasattr(ex, 'args') and len(ex.args) > 0:
            error_code = getattr(ex, 'args')[0]
            if error_code == 208:  # Tabla no encontrada
                codigo_error = 404
            elif error_code in [547, 2627]:  # Violación de restricción o clave duplicada
                codigo_error = 409
                
        mensaje_error = f"Error ({codigo_error}): {str(ex)}"
        return jsonify({"error": mensaje_error}), codigo_error
        
    except Exception as ex:
        # Para otros errores, devolver error 500
        codigo_error = 500
        mensaje_error = f"Error interno del servidor: {str(ex)}"
        traceback.print_exc()  # Imprimir traza completa para depuración
        return jsonify({"error": mensaje_error}), codigo_error

# Obtener un registro específico por clave
@app.route('/api/<string:nombre_proyecto>/<string:nombre_tabla>/<string:nombre_clave>/<string:valor>', methods=['GET'])
def obtener_por_clave(nombre_proyecto, nombre_tabla, nombre_clave, valor):
    """
    Obtiene un registro específico de una tabla, basado en una clave y su valor.
    Es equivalente al método ObtenerPorClave() en EntidadesController.cs.
    
    Args:
        nombre_proyecto (str): Nombre del proyecto al que pertenece la tabla.
        nombre_tabla (str): Nombre de la tabla en la base de datos.
        nombre_clave (str): Nombre de la columna clave utilizada para la búsqueda.
        valor (str): Valor de la clave para filtrar el registro.
        
    Returns:
        JSON: Registro encontrado en formato JSON si la consulta es exitosa, o un código de error en caso de fallo.
    """
    # Verificar si los parámetros están vacíos
    if not nombre_tabla or not nombre_clave or not valor:
        return jsonify({"error": "El nombre de la tabla, el nombre de la clave y el valor no pueden estar vacíos"}), 400
    
    try:
        # Abrir la conexión a la base de datos
        control_conexion.abrir_bd()
        
        # Primero, obtener el tipo de dato de la columna para saber cómo tratar el valor
        consulta_sql = "SELECT data_type FROM information_schema.columns WHERE table_name = @nombreTabla AND column_name = @nombreColumna"
        parametros = [
            control_conexion.crear_parametro("@nombreTabla", nombre_tabla),
            control_conexion.crear_parametro("@nombreColumna", nombre_clave)
        ]
        
        print(f"Ejecutando consulta SQL: {consulta_sql} con parámetros: nombreTabla={nombre_tabla}, nombreColumna={nombre_clave}")
        
        resultado_tipo_dato = control_conexion.ejecutar_consulta_sql(consulta_sql, parametros)
        
        # Verificar si se obtuvo resultado
        if resultado_tipo_dato.empty:
            return jsonify({"error": "No se pudo determinar el tipo de dato"}), 404
        
        # Obtener el tipo de dato
        tipo_dato = resultado_tipo_dato.iloc[0]['data_type']
        print(f"Tipo de dato detectado para la columna {nombre_clave}: {tipo_dato}")
        
        if not tipo_dato:
            return jsonify({"error": "No se pudo determinar el tipo de dato"}), 404
        
        # Convertir el valor según el tipo de dato detectado
        valor_convertido = None
        comando_sql = None
        
        tipo_dato = tipo_dato.lower()
        # Manejar diferentes tipos de datos
        if tipo_dato in ['int', 'bigint', 'smallint', 'tinyint']:
            # Para tipos enteros
            try:
                valor_convertido = int(valor)
                comando_sql = f"SELECT * FROM {nombre_tabla} WHERE {nombre_clave} = @Valor"
            except ValueError:
                return jsonify({"error": "El valor proporcionado no es válido para el tipo de datos entero"}), 400
                
        elif tipo_dato in ['decimal', 'numeric', 'money', 'smallmoney']:
            # Para tipos decimales/monetarios
            try:
                valor_convertido = float(valor)
                comando_sql = f"SELECT * FROM {nombre_tabla} WHERE {nombre_clave} = @Valor"
            except ValueError:
                return jsonify({"error": "El valor proporcionado no es válido para el tipo de datos decimal"}), 400
                
        elif tipo_dato == 'bit':
            # Para tipos booleanos
            valor_lower = valor.lower()
            if valor_lower in ['true', '1', 'yes', 'y']:
                valor_convertido = True
                comando_sql = f"SELECT * FROM {nombre_tabla} WHERE {nombre_clave} = @Valor"
            elif valor_lower in ['false', '0', 'no', 'n']:
                valor_convertido = False
                comando_sql = f"SELECT * FROM {nombre_tabla} WHERE {nombre_clave} = @Valor"
            else:
                return jsonify({"error": "El valor proporcionado no es válido para el tipo de datos booleano"}), 400
                
        elif tipo_dato in ['float', 'real']:
            # Para tipos de punto flotante
            try:
                valor_convertido = float(valor)
                comando_sql = f"SELECT * FROM {nombre_tabla} WHERE {nombre_clave} = @Valor"
            except ValueError:
                return jsonify({"error": "El valor proporcionado no es válido para el tipo de datos flotante"}), 400
                
        elif tipo_dato in ['nvarchar', 'varchar', 'nchar', 'char', 'text']:
            # Para tipos de texto
            valor_convertido = valor
            comando_sql = f"SELECT * FROM {nombre_tabla} WHERE {nombre_clave} = @Valor"
            
        elif tipo_dato in ['date', 'datetime', 'datetime2', 'smalldatetime']:
            # Para tipos de fecha
            try:
                valor_convertido = datetime.datetime.fromisoformat(valor.replace('Z', '+00:00')).date()
                comando_sql = f"SELECT * FROM {nombre_tabla} WHERE CAST({nombre_clave} AS DATE) = @Valor"
            except ValueError:
                return jsonify({"error": "El valor proporcionado no es válido para el tipo de datos fecha"}), 400
                
        else:
            # Para tipos no soportados
            return jsonify({"error": f"Tipo de dato no soportado: {tipo_dato}"}), 400
        
        # Crear el parámetro para la consulta
        parametro = control_conexion.crear_parametro("@Valor", valor_convertido)
        
        print(f"Ejecutando consulta SQL: {comando_sql} con parámetro: Valor = {valor_convertido}")
        
        # Ejecutar la consulta para obtener el registro
        resultado = control_conexion.ejecutar_consulta_sql(comando_sql, [parametro])
        
        # Verificar si hay resultados
        if not resultado.empty:
            # Convertir DataFrame a lista de diccionarios
            lista = resultado.to_dict('records')
            
            # Convertir valores especiales como timestamps y NaN
            for fila in lista:
                for clave, valor in fila.items():
                    if pd.isna(valor):
                        fila[clave] = None
                    elif isinstance(valor, pd.Timestamp):
                        fila[clave] = valor.isoformat()
            
            return jsonify(lista)
        else:
            return jsonify({"error": "No se encontraron registros"}), 404
            
    except Exception as ex:
        print(f"Ocurrió una excepción: {str(ex)}")
        traceback.print_exc()  # Imprimir traza completa para depuración
        return jsonify({"error": f"Error interno del servidor: {str(ex)}"}), 500
        
    finally:
        # Siempre cerrar la conexión, incluso si hay errores
        control_conexion.cerrar_bd()

# Crear un nuevo registro
@app.route('/api/<string:nombre_proyecto>/<string:nombre_tabla>', methods=['POST'])
def crear(nombre_proyecto, nombre_tabla):
    """
    Crea un nuevo registro en la tabla especificada con los datos proporcionados.
    Es equivalente al método Crear() en EntidadesController.cs.
    
    Args:
        nombre_proyecto (str): Nombre del proyecto al que pertenece la tabla.
        nombre_tabla (str): Nombre de la tabla en la base de datos.
        
    Returns:
        JSON: Mensaje de éxito si la inserción es correcta, o un código de error en caso de fallo.
    """
    # Obtener datos del cuerpo de la solicitud JSON
    datos_entidad = request.get_json()
    
    # Verificar si los parámetros están vacíos
    if not nombre_tabla or not datos_entidad:
        return jsonify({"error": "El nombre de la tabla y los datos de la entidad no pueden estar vacíos"}), 400
    
    try:
        # Convertir los datos recibidos a sus tipos apropiados
        propiedades = {}
        for clave, valor in datos_entidad.items():
            propiedades[clave] = convertir_json_element(valor)
        
        # Verificar si hay campos de contraseña para aplicar hash
        claves_contrasena = ['password', 'contrasena', 'passw', 'clave']
        clave_contrasena = None
        
        # Buscar si alguna clave contiene palabras relacionadas con contraseñas
        for clave in propiedades.keys():
            if any(pk in clave.lower() for pk in claves_contrasena):
                clave_contrasena = clave
                break
        
        # Si se encuentra un campo de contraseña, cifrarla con bcrypt
        if clave_contrasena and propiedades[clave_contrasena]:
            contrasena_plano = str(propiedades[clave_contrasena])
            propiedades[clave_contrasena] = bcrypt.hashpw(contrasena_plano.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Obtener el proveedor de base de datos desde la configuración
        proveedor = datos_config.get("DatabaseProvider")
        if not proveedor:
            raise ValueError("Proveedor de base de datos no configurado")
        
        # Construir la consulta SQL de inserción
        columnas = ", ".join(propiedades.keys())  # Lista de columnas separadas por comas
        prefijo = obtener_prefijo_parametro(proveedor)  # @ para SQL Server
        valores = ", ".join([f"{prefijo}{k}" for k in propiedades.keys()])  # Lista de parámetros (@columna1, @columna2, ...)
        
        consulta_sql = f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores})"
        
        # Crear los parámetros para la consulta SQL
        parametros = [control_conexion.crear_parametro(f"{prefijo}{clave}", valor) for clave, valor in propiedades.items()]
        
        # Mostrar la consulta y parámetros (para depuración)
        print(f"Ejecutando consulta SQL: {consulta_sql}")
        for param in parametros:
            print(f"Parámetro: {param[0]} = {param[1]}")
        
        # Ejecutar la consulta
        control_conexion.abrir_bd()
        control_conexion.ejecutar_comando_sql(consulta_sql, parametros)
        control_conexion.cerrar_bd()
        
        return jsonify({"mensaje": "Entidad creada exitosamente"})
        
    except Exception as ex:
        print(f"Ocurrió una excepción: {str(ex)}")
        traceback.print_exc()  # Imprimir traza completa para depuración
        return jsonify({"error": f"Error interno del servidor: {str(ex)}"}), 500

# Actualizar un registro existente
@app.route('/api/<string:nombre_proyecto>/<string:nombre_tabla>/<string:nombre_clave>/<string:valor_clave>', methods=['PUT'])
def actualizar(nombre_proyecto, nombre_tabla, nombre_clave, valor_clave):
    """
    Actualiza un registro específico en la tabla de la base de datos basado en una clave y su valor.
    Es equivalente al método Actualizar() en EntidadesController.cs.
    
    Args:
        nombre_proyecto (str): Nombre del proyecto al que pertenece la tabla.
        nombre_tabla (str): Nombre de la tabla en la base de datos.
        nombre_clave (str): Nombre de la columna clave utilizada para la búsqueda.
        valor_clave (str): Valor de la clave para identificar el registro a actualizar.
        
    Returns:
        JSON: Mensaje de éxito si la actualización es correcta, o un código de error en caso de fallo.
    """
    # Obtener datos del cuerpo de la solicitud JSON
    datos_entidad = request.get_json()
    
    # Verificar si los parámetros están vacíos
    if not nombre_tabla or not nombre_clave or not datos_entidad:
        return jsonify({"error": "El nombre de la tabla, el nombre de la clave y los datos de la entidad no pueden estar vacíos"}), 400
    
    try:
        # Convertir los datos recibidos a sus tipos apropiados
        propiedades = {}
        for clave, valor in datos_entidad.items():
            propiedades[clave] = convertir_json_element(valor)
        
        # Verificar si hay campos de contraseña para aplicar hash
        claves_contrasena = ['password', 'contrasena', 'passw', 'clave']
        clave_contrasena = None
        
        # Buscar si alguna clave contiene palabras relacionadas con contraseñas
        for clave in propiedades.keys():
            if any(pk in clave.lower() for pk in claves_contrasena):
                clave_contrasena = clave
                break
        
        # Si se encuentra un campo de contraseña, cifrarla con bcrypt
        if clave_contrasena and propiedades[clave_contrasena]:
            contrasena_plano = str(propiedades[clave_contrasena])
            propiedades[clave_contrasena] = bcrypt.hashpw(contrasena_plano.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Obtener el proveedor de base de datos desde la configuración
        proveedor = datos_config.get("DatabaseProvider")
        if not proveedor:
            raise ValueError("Proveedor de base de datos no configurado")
        
        # Construir la consulta SQL de actualización
        prefijo = obtener_prefijo_parametro(proveedor)  # @ para SQL Server
        # Crear la parte SET de la consulta: "columna1=@columna1, columna2=@columna2"
        actualizaciones = ", ".join([f"{clave}={prefijo}{clave}" for clave in propiedades.keys()])
        
        # Armar la consulta completa
        consulta_sql = f"UPDATE {nombre_tabla} SET {actualizaciones} WHERE {nombre_clave}={prefijo}ValorClave"
        
        # Crear los parámetros para la consulta SQL
        parametros = [control_conexion.crear_parametro(f"{prefijo}{clave}", valor) for clave, valor in propiedades.items()]
        # Añadir el parámetro para la clave
        parametros.append(control_conexion.crear_parametro(f"{prefijo}ValorClave", valor_clave))
        
        # Mostrar la consulta y parámetros (para depuración)
        print(f"Ejecutando consulta SQL: {consulta_sql}")
        for param in parametros:
            print(f"Parámetro: {param[0]} = {param[1]}")
        
        # Ejecutar la consulta
        control_conexion.abrir_bd()
        control_conexion.ejecutar_comando_sql(consulta_sql, parametros)
        control_conexion.cerrar_bd()
        
        return jsonify({"mensaje": "Entidad actualizada exitosamente"})
        
    except Exception as ex:
        print(f"Ocurrió una excepción: {str(ex)}")
        traceback.print_exc()  # Imprimir traza completa para depuración
        return jsonify({"error": f"Error interno del servidor: {str(ex)}"}), 500

# Eliminar un registro
@app.route('/api/<string:nombre_proyecto>/<string:nombre_tabla>/<string:nombre_clave>/<string:valor_clave>', methods=['DELETE'])
def eliminar(nombre_proyecto, nombre_tabla, nombre_clave, valor_clave):
    """
    Elimina un registro específico de la tabla de la base de datos basado en una clave y su valor.
    Es equivalente al método Eliminar() en EntidadesController.cs.
    
    Args:
        nombre_proyecto (str): Nombre del proyecto al que pertenece la tabla.
        nombre_tabla (str): Nombre de la tabla en la base de datos.
        nombre_clave (str): Nombre de la columna clave utilizada para identificar el registro.
        valor_clave (str): Valor de la clave que identifica el registro a eliminar.
        
    Returns:
        JSON: Mensaje de éxito si la eliminación es correcta, o un código de error en caso de fallo.
    """
    # Verificar si los parámetros están vacíos
    if not nombre_tabla or not nombre_clave:
        return jsonify({"error": "El nombre de la tabla o el nombre de la clave no pueden estar vacíos"}), 400
    
    try:
        # Obtener el proveedor de base de datos
        proveedor = datos_config.get("DatabaseProvider")
        if not proveedor:
            raise ValueError("Proveedor de base de datos no configurado")
        
        # Construir la consulta SQL de eliminación
        consulta_sql = f"DELETE FROM {nombre_tabla} WHERE {nombre_clave}=@ValorClave"
        
        # Crear el parámetro para la clave
        parametro = control_conexion.crear_parametro("@ValorClave", valor_clave)
        
        # Ejecutar la consulta
        control_conexion.abrir_bd()
        control_conexion.ejecutar_comando_sql(consulta_sql, [parametro])
        control_conexion.cerrar_bd()
        
        return jsonify({"mensaje": "Entidad eliminada exitosamente"})
        
    except Exception as ex:
        print(f"Ocurrió una excepción: {str(ex)}")
        return jsonify({"error": f"Error interno del servidor: {str(ex)}"}), 500

# Verificar contraseña
@app.route('/api/<string:nombre_proyecto>/<string:nombre_tabla>/verificar-contrasena', methods=['POST'])
def verificar_contrasena(nombre_proyecto, nombre_tabla):
    """
    Verifica si la contraseña proporcionada coincide con la contraseña almacenada en la base de datos para un usuario específico.
    Es equivalente al método VerificarContrasena() en EntidadesController.cs.
    
    Args:
        nombre_proyecto (str): Nombre del proyecto al que pertenece la tabla.
        nombre_tabla (str): Nombre de la tabla en la base de datos que almacena los usuarios.
        
    Returns:
        JSON: Mensaje indicando el resultado de la verificación.
    """
    # Obtener datos del cuerpo de la solicitud
    datos = request.get_json()
    
    # Verificar si los parámetros están vacíos o faltan campos requeridos
    if not nombre_tabla or not datos or \
       'campoUsuario' not in datos or 'campoContrasena' not in datos or \
       'valorUsuario' not in datos or 'valorContrasena' not in datos:
        return jsonify({
            "error": "El nombre de la tabla, el campo de usuario, el campo de contraseña, el valor de usuario y el valor de contraseña no pueden estar vacíos"
        }), 400
    
    try:
        # Extraer los valores necesarios del request
        campo_usuario = datos['campoUsuario']  # Nombre de la columna que contiene el usuario
        campo_contrasena = datos['campoContrasena']  # Nombre de la columna que contiene la contraseña
        valor_usuario = datos['valorUsuario']  # Valor del usuario a buscar
        valor_contrasena = datos['valorContrasena']  # Contraseña a verificar
        
        # Obtener el proveedor de base de datos
        proveedor = datos_config.get("DatabaseProvider")
        if not proveedor:
            raise ValueError("Proveedor de base de datos no configurado")
        
        # Construir la consulta SQL para obtener la contraseña almacenada
        consulta_sql = f"SELECT {campo_contrasena} FROM {nombre_tabla} WHERE {campo_usuario} = @ValorUsuario"
        
        # Crear el parámetro para el usuario
        parametro = control_conexion.crear_parametro("@ValorUsuario", valor_usuario)
        
        # Ejecutar la consulta
        control_conexion.abrir_bd()
        resultado = control_conexion.ejecutar_consulta_sql(consulta_sql, [parametro])
        control_conexion.cerrar_bd()
        
        # Verificar si se encontró el usuario
        if resultado.empty:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        # Obtener la contraseña almacenada (hash bcrypt)
        contrasena_hasheada = resultado.iloc[0][campo_contrasena]
        
        # Verificar que sea un hash bcrypt válido (debe empezar con $2)
        if not contrasena_hasheada or not str(contrasena_hasheada).startswith('$2'):
            raise ValueError("El hash de la contraseña almacenada no es un hash válido de BCrypt")
        
        # Verificar la contraseña utilizando bcrypt
        es_contrasena_valida = bcrypt.checkpw(
            valor_contrasena.encode('utf-8'),  # Convertir a bytes la contraseña proporcionada
            str(contrasena_hasheada).encode('utf-8')  # Convertir a bytes el hash almacenado
        )
        
        if es_contrasena_valida:
            return jsonify({"mensaje": "Contraseña verificada exitosamente"})
        else:
            return jsonify({"error": "Contraseña incorrecta"}), 401
            
    except Exception as ex:
        print(f"Ocurrió una excepción: {str(ex)}")
        return jsonify({"error": f"Error interno del servidor: {str(ex)}"}), 500

# Ejecutar consulta parametrizada
@app.route('/api/<string:nombre_proyecto>/<string:nombre_tabla>/ejecutar-consulta-parametrizada', methods=['POST'])
def ejecutar_consulta_parametrizada(nombre_proyecto, nombre_tabla):
    """
    Ejecuta una consulta SQL parametrizada recibida en el cuerpo de la solicitud.
    Es equivalente al método EjecutarConsultaParametrizada() en EntidadesController.cs.
    
    Args:
        nombre_proyecto (str): Nombre del proyecto al que pertenece la tabla.
        nombre_tabla (str): Nombre de la tabla en la base de datos.
        
    Returns:
        JSON: Resultados de la consulta en formato JSON o un mensaje de error en caso de fallo.
    """
    # Obtener datos del cuerpo de la solicitud
    cuerpo_solicitud = request.get_json()
    
    # Verificar si se proporcionó la consulta
    if not cuerpo_solicitud or 'consulta' not in cuerpo_solicitud or not cuerpo_solicitud['consulta']:
        return jsonify({"error": "Debe proporcionar una consulta SQL válida en el cuerpo de la solicitud"}), 400
    
    try:
        # Extraer la consulta SQL
        consulta_sql = cuerpo_solicitud['consulta']
        
        # Verificar si hay parámetros y procesarlos
        parametros = []
        if 'parametros' in cuerpo_solicitud and isinstance(cuerpo_solicitud['parametros'], dict):
            for nombre, valor in cuerpo_solicitud['parametros'].items():
                # Asegurar que el nombre del parámetro comience con @
                nombre_param = nombre if nombre.startswith('@') else '@' + nombre
                parametros.append(control_conexion.crear_parametro(nombre_param, valor))
        
        # Ejecutar la consulta
        control_conexion.abrir_bd()
        resultado = control_conexion.ejecutar_consulta_sql(consulta_sql, parametros)
        control_conexion.cerrar_bd()
        
        # Verificar si hay resultados
        if resultado.empty:
            return jsonify({"error": "No se encontraron resultados para la consulta proporcionada"}), 404
        
        # Convertir DataFrame a lista de diccionarios
        lista = resultado.to_dict('records')
        
        # Convertir valores especiales como timestamps y NaN
        for fila in lista:
            for clave, valor in fila.items():
                if pd.isna(valor):
                    fila[clave] = None
                elif isinstance(valor, pd.Timestamp):
                    fila[clave] = valor.isoformat()
        
        return jsonify(lista)
        
    except pyodbc.Error as ex:
        # Cerrar la conexión en caso de error
        control_conexion.cerrar_bd()
        print(f"SQL Error: {str(ex)}")
        return jsonify({"error": f"Error en la base de datos: {str(ex)}"}), 500
        
    except Exception as ex:
        # Cerrar la conexión en caso de error
        control_conexion.cerrar_bd()
        print(f"Error: {str(ex)}")
        return jsonify({"error": f"Se presentó un error: {str(ex)}"}), 500

# Punto de entrada para ejecutar la aplicación (equivalente a app.Run())
if __name__ == '__main__':
    # Determinar si estamos en modo desarrollo
    entorno_desarrollo = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    # Configurar la aplicación según el entorno (equivalente a if (app.Environment.IsDevelopment()))
    if entorno_desarrollo:
        # Modo desarrollo: mostrar errores detallados y habilitar recarga automática
        debug_mode = True
        
        # Mensaje informativo sobre el modo desarrollo
        print("API en modo DESARROLLO - No usar en producción")
    else:
        # Modo producción: ocultar errores detallados y deshabilitar recarga automática
        debug_mode = False
        
        # Mensaje informativo sobre el modo producción
        print("API en modo PRODUCCIÓN")
    
    # Iniciar el servidor de desarrollo de Flask
    # El puerto predeterminado es 5000, pero puede cambiarse
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
    
    # Para cambiar el puerto, modificar el parámetro port:
    # app.run(debug=debug_mode, port=8080)

"""
Modos de uso:

GET
http://localhost:5184/api/proyecto/usuario
http://localhost:5184/api/proyecto/usuario/email/admin@empresa.com

POST
http://localhost:5184/api/proyecto/usuario/
{
    "email": "nuevo.nuevo@empresa.com",
    "contrasena": "123"
}

PUT
http://localhost:5184/api/proyecto/usuario/email/nuevo.nuevo@empresa.com
{
    "contrasena": "456"
}

DELETE
http://localhost:5184/api/proyecto/usuario/email/nuevo.nuevo@empresa.com
*/
/*
Códigos de estado HTTP:

2xx (Éxito):
- 200 OK: La solicitud ha tenido éxito.
- 201 Creado: La solicitud ha sido completada y ha resultado en la creación de un nuevo recurso.
- 202 Aceptado: La solicitud ha sido aceptada para procesamiento, pero el procesamiento no ha sido completado.
- 203 Información no autoritativa: La respuesta se ha obtenido de una copia en caché en lugar de directamente del servidor original.
- 204 Sin contenido: La solicitud ha tenido éxito pero no hay contenido que devolver.
- 205 Restablecer contenido: La solicitud ha tenido éxito, pero el cliente debe restablecer la vista que ha solicitado.
- 206 Contenido parcial: El servidor está enviando una respuesta parcial del recurso debido a una solicitud Range.

3xx (Redirección):
- 300 Múltiples opciones: El servidor puede responder con una de varias opciones.
- 301 Movido permanentemente: El recurso solicitado ha sido movido de manera permanente a una nueva URL.
- 302 Encontrado: El recurso solicitado reside temporalmente en una URL diferente.
- 303 Ver otros: El servidor dirige al cliente a una URL diferente para obtener la respuesta solicitada (usualmente en una operación POST).
- 304 No modificado: El contenido no ha cambiado desde la última solicitud (usualmente usado con la caché).
- 305 Usar proxy: El recurso solicitado debe ser accedido a través de un proxy.
- 307 Redirección temporal: Similar al 302, pero el cliente debe utilizar el mismo método de solicitud original (GET o POST).
- 308 Redirección permanente: Similar al 301, pero el método de solicitud original debe ser utilizado en la nueva URL.

4xx (Errores del cliente):
- 400 Solicitud incorrecta: La solicitud contiene sintaxis errónea o no puede ser procesada.
- 401 No autorizado: El cliente debe autenticarse para obtener la respuesta solicitada.
- 402 Pago requerido: Este código es reservado para uso futuro, generalmente relacionado con pagos.
- 403 Prohibido: El cliente no tiene permisos para acceder al recurso, incluso si está autenticado.
- 404 No encontrado: El servidor no pudo encontrar el recurso solicitado.
- 405 Método no permitido: El método HTTP utilizado no está permitido para el recurso solicitado.
- 406 No aceptable: El servidor no puede generar una respuesta que coincida con las características aceptadas por el cliente.
- 407 Autenticación de proxy requerida: Similar a 401, pero la autenticación debe hacerse a través de un proxy.
- 408 Tiempo de espera agotado: El cliente no envió una solicitud dentro del tiempo permitido por el servidor.
- 409 Conflicto: La solicitud no pudo ser completada debido a un conflicto en el estado actual del recurso.
- 410 Gone: El recurso solicitado ya no está disponible y no será vuelto a crear.
- 411 Longitud requerida: El servidor requiere que la solicitud especifique una longitud en los encabezados.
- 412 Precondición fallida: Una condición en los encabezados de la solicitud falló.
- 413 Carga útil demasiado grande: El cuerpo de la solicitud es demasiado grande para ser procesado.
- 414 URI demasiado largo: La URI solicitada es demasiado larga para que el servidor la procese.
- 415 Tipo de medio no soportado: El formato de los datos en la solicitud no es compatible con el servidor.
- 416 Rango no satisfactorio: La solicitud incluye un rango que no puede ser satisfecho.
- 417 Fallo en la expectativa: La expectativa indicada en los encabezados de la solicitud no puede ser cumplida.
- 418 Soy una tetera (RFC 2324): Este código es un Easter Egg HTTP. El servidor rechaza la solicitud porque "soy una tetera."
- 421 Mala asignación: El servidor no puede cumplir con la solicitud.
- 426 Se requiere actualización: El cliente debe actualizar el protocolo de solicitud.
- 428 Precondición requerida: El servidor requiere que se cumpla una precondición antes de procesar la solicitud.
- 429 Demasiadas solicitudes: El cliente ha enviado demasiadas solicitudes en un corto periodo de tiempo.
- 431 Campos de encabezado muy grandes: Los campos de encabezado de la solicitud son demasiado grandes.
- 451 No disponible por razones legales: El contenido ha sido bloqueado por razones legales (ej. leyes de copyright).

5xx (Errores del servidor):
- 500 Error interno del servidor: El servidor encontró una situación inesperada que le impidió completar la solicitud.
- 501 No implementado: El servidor no tiene la capacidad de completar la solicitud.
- 502 Puerta de enlace incorrecta: El servidor, al actuar como puerta de enlace o proxy, recibió una respuesta no válida del servidor upstream.
- 503 Servicio no disponible: El servidor no está disponible temporalmente, generalmente debido a mantenimiento o sobrecarga.
- 504 Tiempo de espera de la puerta de enlace: El servidor, al actuar como puerta de enlace o proxy, no recibió una respuesta a tiempo de otro servidor.
- 505 Versión HTTP no soportada: El servidor no soporta la versión HTTP utilizada en la solicitud.
- 506 Variante también negocia: El servidor encontró una referencia circular al negociar el contenido.
- 507 Almacenamiento insuficiente: El servidor no puede almacenar la representación necesaria para completar la solicitud.
- 508 Bucle detectado: El servidor detectó un bucle infinito al procesar la solicitud.
- 510 No extendido: Se requiere la extensión adicional de las políticas de acceso.
- 511 Se requiere autenticación de red: El cliente debe autenticar la red para poder acceder al recurso.
"""
