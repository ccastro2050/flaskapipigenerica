# servicios/token_service.py
# Equivalente a TokenService.cs en una API de C#

import datetime
import json
import os
import uuid
import jwt  # Se requiere instalar: pip install PyJWT

class TokenService:
    """
    Clase que gestiona la creación y validación de tokens JWT.
    Equivalente a la clase TokenService en C#.
    """
    
    def __init__(self, configuracion=None):
        """
        Constructor de la clase.
        Carga la configuración JWT.
        
        Args:
            configuracion: Configuración de la aplicación. Si es None, se carga desde el archivo.
        """
        # Verificar si se proporcionó la configuración
        if configuracion is None:
            # Si no se proporcionó, cargar desde el archivo
            try:
                ruta_config = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configuracion', 'config.json')
                with open(ruta_config) as archivo_config:
                    self.configuracion = json.load(archivo_config)
            except Exception as e:
                raise ValueError(f"No se pudo cargar la configuración: {str(e)}")
        else:
            # Si se proporcionó, usarla directamente
            self.configuracion = configuracion
    
    def generar_token(self, usuario):
        """
        Genera un token JWT para un usuario.
        Equivalente a GenerarToken(string usuario) en C#.
        
        Args:
            usuario (str): Nombre o identificador del usuario.
            
        Returns:
            str: Token JWT generado.
        """
        # Obtener la clave JWT desde la configuración
        clave_jwt = self.configuracion.get("Jwt", {}).get("Key")
        if not clave_jwt:
            raise ValueError("La clave JWT no está configurada correctamente")
        
        # Obtener el emisor y la audiencia
        emisor = self.configuracion.get("Jwt", {}).get("Issuer")
        audiencia = self.configuracion.get("Jwt", {}).get("Audience")
        
        # Crear claims (equivalente a claims en C#)
        claims = {
            "sub": usuario,  # Subject (usuario)
            "jti": str(uuid.uuid4()),  # JWT ID (identificador único del token)
            "iss": emisor,  # Issuer (emisor)
            "aud": audiencia,  # Audience (audiencia)
            "iat": datetime.datetime.utcnow(),  # Issued At (momento de emisión)
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)  # Expiration (2 horas desde ahora)
        }
        
        # Generar el token
        token = jwt.encode(
            claims,
            clave_jwt,
            algorithm="HS256"
        )
        
        return token
    
    def validar_token(self, token):
        """
        Valida un token JWT.
        Esta función no está en el TokenService.cs original pero es útil.
        
        Args:
            token (str): Token JWT a validar.
            
        Returns:
            dict: Payload del token si es válido.
            None: Si el token es inválido.
        """
        try:
            # Obtener la clave JWT desde la configuración
            clave_jwt = self.configuracion.get("Jwt", {}).get("Key")
            if not clave_jwt:
                raise ValueError("La clave JWT no está configurada correctamente")
            
            # Obtener el emisor y la audiencia
            emisor = self.configuracion.get("Jwt", {}).get("Issuer")
            audiencia = self.configuracion.get("Jwt", {}).get("Audience")
            
            # Verificar el token
            payload = jwt.decode(
                token,
                clave_jwt,
                algorithms=["HS256"],
                options={"verify_signature": True, "verify_exp": True},
                issuer=emisor,
                audience=audiencia
            )
            
            return payload
        except jwt.ExpiredSignatureError:
            print("Token expirado")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Token inválido: {str(e)}")
            return None