# servicios/control_conexion.py
# Equivalente a ControlConexion.cs en una API de C#

import os
import json
import pyodbc  # Equivalente a Microsoft.Data.SqlClient
import pandas as pd  # Para manejar datos de manera similar a DataTable
from sqlalchemy import create_engine  # Para conexiones a través de SQLAlchemy

class ControlConexion:
    """
    Clase que gestiona las conexiones a la base de datos.
    Equivalente a la clase ControlConexion en C#.
    """
    
    def __init__(self, entorno=None, configuracion=None):
        """
        Constructor de la clase.
        Inicializa el entorno y la configuración.
        
        Args:
            entorno: Objeto que contiene información sobre el entorno de la aplicación.
            configuracion: Configuración de la aplicación.
        """
        # En Python, verificamos si los argumentos son None en lugar de lanzar ArgumentNullException
        if entorno is None:
            # Para simplificar, permitimos que entorno sea None en este ejemplo
            pass
        
        if configuracion is None:
            # Si no se proporciona configuración, intentamos cargarla del archivo
            ruta_config = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configuracion', 'config.json')
            try:
                with open(ruta_config) as archivo_config:
                    self.configuracion = json.load(archivo_config)
            except Exception as e:
                raise ValueError(f"No se pudo cargar la configuración: {str(e)}")
        else:
            self.configuracion = configuracion
        
        self.entorno = entorno
        self.conexion_bd = None  # Equivalente a _conexionBd
    
    def abrir_bd(self):
        """
        Método para abrir la base de datos, compatible con SQL Server.
        Equivalente a AbrirBd() en C#.
        """
        try:
            # Obtener el proveedor desde la configuración
            proveedor = self.configuracion.get("DatabaseProvider")
            if not proveedor:
                raise ValueError("Proveedor de base de datos no configurado")
            
            # Obtener la cadena de conexión
            cadena_conexion = self.configuracion.get("ConnectionStrings", {}).get(proveedor)
            if not cadena_conexion:
                raise ValueError("La cadena de conexión es nula o vacía")
            
            print(f"Intentando abrir conexión con el proveedor: {proveedor}")
            print(f"Cadena de conexión: {cadena_conexion}")
            
            # Crear la conexión según el proveedor
            if proveedor == "LocalDb":
                # LocalDB usa pyodbc en Python
                try:
                    self.conexion_bd = pyodbc.connect(cadena_conexion, autocommit=True)
                except pyodbc.Error as e:
                    print(f"Error al conectar a LocalDb: {str(e)}")
                    raise
            elif proveedor == "SqlServer":
                # SQL Server usa pyodbc en Python
                try:
                    self.conexion_bd = pyodbc.connect(cadena_conexion, autocommit=True)
                except pyodbc.Error as e:
                    print(f"Error al conectar a SQL Server: {str(e)}")
                    raise
            else:
                raise ValueError(f"Proveedor de base de datos no soportado: {proveedor}. Solo se admiten LocalDb y SqlServer")
            
            print("Conexión a la base de datos abierta exitosamente")
        except pyodbc.Error as ex:
            print(f"Ocurrió un error de SQL: {str(ex)}")
            # En Python no tenemos propiedades como Number, State y Class como en SqlException
            # pero podemos obtener información similar
            if hasattr(ex, 'args'):
                for i, arg in enumerate(ex.args):
                    print(f"Argumento {i}: {arg}")
            raise ValueError(f"Error al abrir la conexión a la base de datos debido a un error SQL: {str(ex)}")
        except Exception as ex:
            print(f"Ocurrió una excepción: {str(ex)}")
            raise ValueError(f"Error al abrir la conexión a la base de datos: {str(ex)}")
    
    def abrir_bd_localdb(self, archivo_bd):
        """
        Método específico para abrir una base de datos LocalDB.
        Equivalente a AbrirBdLocalDB(string archivoBd) en C#.
        
        Args:
            archivo_bd (str): Nombre del archivo de base de datos.
        """
        try:
            # Verificar si el nombre del archivo termina en .mdf
            nombre_archivo_bd = archivo_bd if archivo_bd.endswith(".mdf") else archivo_bd + ".mdf"
            
            # Definir la ruta completa al archivo
            ruta_app_data = os.path.join(os.path.dirname(os.path.dirname(__file__)), "App_Data")
            ruta_archivo = os.path.join(ruta_app_data, nombre_archivo_bd)
            
            # Crear la cadena de conexión para LocalDB
            cadena_conexion = f"DRIVER={{SQL Server}};SERVER=(LocalDB)\\MSSQLLocalDB;AttachDbFilename={ruta_archivo};Integrated Security=True"
            
            # Abrir la conexión
            self.conexion_bd = pyodbc.connect(cadena_conexion, autocommit=True)
        except Exception as ex:
            raise ValueError(f"Error al abrir la conexión a LocalDB: {str(ex)}")
    
    def cerrar_bd(self):
        """
        Método para cerrar la conexión a la base de datos.
        Equivalente a CerrarBd() en C#.
        """
        try:
            # Verificar si la conexión está abierta y cerrarla
            if self.conexion_bd is not None:
                self.conexion_bd.close()
                self.conexion_bd = None
        except Exception as ex:
            raise ValueError(f"Error al cerrar la conexión a la base de datos: {str(ex)}")
    
    def ejecutar_comando_sql(self, consulta_sql, parametros):
        """
        Método para ejecutar un comando SQL y devolver el número de filas afectadas.
        Equivalente a EjecutarComandoSql(string consultaSql, DbParameter[] parametros) en C#.
        
        Args:
            consulta_sql (str): Consulta SQL a ejecutar.
            parametros (list): Lista de parámetros para la consulta.
            
        Returns:
            int: Número de filas afectadas.
        """
        try:
            # Verificar si la conexión está abierta
            if self.conexion_bd is None:
                raise ValueError("La conexión a la base de datos no está abierta")
            
            # Crear y ejecutar el comando
            cursor = self.conexion_bd.cursor()
            params_values = []
            
            # Los parámetros en Python son simples tuplas (nombre, valor)
            for parametro in parametros:
                print(f"Agregando parámetro: {parametro[0]} = {parametro[1]}")
                params_values.append(parametro[1])
            
            # Ejecutar la consulta con los parámetros
            cursor.execute(consulta_sql, params_values)
            
            # Obtener el número de filas afectadas
            filas_afectadas = cursor.rowcount
            cursor.close()
            
            return filas_afectadas
        except Exception as ex:
            print(f"Ocurrió una excepción: {str(ex)}")
            raise ValueError(f"Error al ejecutar el comando SQL: {str(ex)}")
    
    def ejecutar_consulta_sql(self, consulta_sql, parametros=None):
        """
        Método para ejecutar una consulta SQL y devolver un DataFrame con los resultados.
        Equivalente a EjecutarConsultaSql(string consultaSql, DbParameter[]? parametros) en C#.
        
        Args:
            consulta_sql (str): Consulta SQL a ejecutar.
            parametros (list, optional): Lista de parámetros para la consulta.
            
        Returns:
            pandas.DataFrame: Resultados de la consulta como un DataFrame.
        """
        # Verificar si la conexión está abierta
        if self.conexion_bd is None:
            raise ValueError("La conexión a la base de datos no está abierta")
        
        try:
            # Crear y ejecutar el comando
            cursor = self.conexion_bd.cursor()
            params_values = []
            
            # Procesar parámetros si los hay
            if parametros is not None:
                for param in parametros:
                    print(f"Agregando parámetro: {param[0]} = {param[1]}")
                    params_values.append(param[1])
                
                # Ejecutar la consulta con los parámetros
                cursor.execute(consulta_sql, params_values)
            else:
                # Ejecutar la consulta sin parámetros
                cursor.execute(consulta_sql)
            
            # Obtener los nombres de las columnas
            columnas = [column[0] for column in cursor.description]
            
            # Obtener todas las filas
            filas = cursor.fetchall()
            
            # Verificar si hay resultados
            if not filas:
                print("No se devolvieron filas en la consulta")
                return pd.DataFrame(columns=columnas)
            
            # Crear un DataFrame con los resultados
            df = pd.DataFrame.from_records(filas, columns=columnas)
            
            print(f"Número de filas en el resultado: {len(df)}")
            
            return df
        except Exception as ex:
            print(f"Ocurrió una excepción: {str(ex)}")
            raise Exception(f"Error al ejecutar la consulta SQL. Error: {str(ex)}")
    
    def crear_parametro(self, nombre, valor):
        """
        Método para crear un parámetro de consulta SQL.
        Equivalente a CrearParametro(string nombre, object? valor) en C#.
        
        Args:
            nombre (str): Nombre del parámetro.
            valor (object): Valor del parámetro.
            
        Returns:
            tuple: Tupla con el nombre y valor del parámetro.
        """
        try:
            # Obtener el proveedor desde la configuración
            proveedor = self.configuracion.get("DatabaseProvider")
            if not proveedor:
                raise ValueError("Proveedor de base de datos no configurado")
            
            # En Python, los parámetros son más simples que en C#
            # Solo necesitamos devolver una tupla con el nombre y el valor
            return (nombre, valor if valor is not None else None)
        except Exception as ex:
            raise ValueError(f"Error al crear el parámetro: {str(ex)}")
    
    def obtener_conexion(self):
        """
        Método para obtener la conexión actual a la base de datos.
        Equivalente a ObtenerConexion() en C#.
        
        Returns:
            Connection: Objeto de conexión a la base de datos.
        """
        return self.conexion_bd
    
    def ejecutar_procedimiento_almacenado(self, nombre_procedimiento, parametros=None):
        """
        Método para ejecutar un procedimiento almacenado y devolver un DataFrame con los resultados.
        Equivalente a EjecutarProcedimientoAlmacenado(string nombreProcedimiento, DbParameter[]? parametros) en C#.
        
        Args:
            nombre_procedimiento (str): Nombre del procedimiento almacenado.
            parametros (list, optional): Lista de parámetros para el procedimiento.
            
        Returns:
            pandas.DataFrame: Resultados del procedimiento almacenado como un DataFrame.
        """
        if self.conexion_bd is None:
            raise ValueError("La conexión no está abierta")
        
        try:
            # Crear cursor
            cursor = self.conexion_bd.cursor()
            
            # Preparar los parámetros
            params_values = []
            if parametros is not None:
                for param in parametros:
                    params_values.append(param[1])
            
            # Construir la llamada al procedimiento almacenado
            # En SQL Server, se usa {call nombre_proc(?, ?, ...)}
            param_placeholders = ",".join(["?" for _ in range(len(params_values))])
            sql = f"{{call {nombre_procedimiento}({param_placeholders})}}"
            
            # Ejecutar el procedimiento
            cursor.execute(sql, params_values)
            
            # Obtener los nombres de las columnas
            columnas = [column[0] for column in cursor.description]
            
            # Obtener todas las filas
            filas = cursor.fetchall()
            
            # Crear un DataFrame con los resultados
            df = pd.DataFrame.from_records(filas, columns=columnas)
            
            return df
        except Exception as ex:
            raise Exception(f"Error al ejecutar el procedimiento almacenado: {str(ex)}")
    
    def ejecutar_funcion(self, nombre_funcion, parametros=None):
        """
        Método para ejecutar una función SQL y devolver un resultado escalar.
        Equivalente a EjecutarFuncion(string nombreFuncion, DbParameter[]? parametros) en C#.
        
        Args:
            nombre_funcion (str): Nombre de la función SQL.
            parametros (list, optional): Lista de parámetros para la función.
            
        Returns:
            object: Resultado escalar de la función SQL.
        """
        if self.conexion_bd is None:
            raise ValueError("La conexión no está abierta")
        
        try:
            # Crear cursor
            cursor = self.conexion_bd.cursor()
            
            # Preparar los parámetros
            params_values = []
            if parametros is not None:
                for param in parametros:
                    params_values.append(param[1])
            
            # Construir la llamada a la función
            # En SQL Server, se usa SELECT dbo.nombre_funcion(?, ?, ...)
            param_placeholders = ",".join(["?" for _ in range(len(params_values))])
            sql = f"SELECT {nombre_funcion}({param_placeholders})"
            
            # Ejecutar la función
            cursor.execute(sql, params_values)
            
            # Obtener el resultado escalar
            resultado = cursor.fetchone()[0]
            
            return resultado
        except Exception as ex:
            raise Exception(f"Error al ejecutar la función SQL: {str(ex)}")