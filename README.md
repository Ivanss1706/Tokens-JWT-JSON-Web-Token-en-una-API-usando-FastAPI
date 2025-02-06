# Tokens-JWT-JSON-Web-Token-en-una-API-usando-FastAPI
Este código es un ejemplo de cómo implementar autenticación de usuario con tokens JWT (JSON Web Token) en una API usando FastAPI.

## 1. Configuración de Dependencias

*   Se utilizan las siguientes librerías:
    *   `python-jose`: Para generar y verificar tokens JWT.
    *   `passlib`: Para encriptar y verificar contraseñas usando el algoritmo bcrypt.
    *   `fastapi`: Como framework para crear la API y gestionar las rutas.

## 2. Modelos de Datos

*   Se definen los siguientes modelos:
    *   `User`: Contiene atributos del usuario como nombre de usuario, nombre completo, email y estado (`disabled`).
    *   `UserDB`: Extiende el modelo `User` e incluye la contraseña encriptada.
    *   `equipo`: Un modelo simplificado con solo nombre de usuario y estado.

## 3. Base de Datos de Usuarios (Simulada)

*   `users_db`: Un diccionario que simula una base de datos con usuarios y sus contraseñas encriptadas.

## 4. Funciones

*   `search_user_db`: Busca un usuario por nombre de usuario y devuelve todos sus atributos, incluyendo la contraseña encriptada.
*   `search_user`: Devuelve un usuario sin la contraseña (solo atributos públicos).
*   `auth_user`: Valida el token JWT de la solicitud, lo decodifica y devuelve el usuario correspondiente.
*   `current_user`: Verifica si el usuario está activo (`disabled` es False).
*   `login`: Endpoint de autenticación. Recibe nombre de usuario y contraseña, verifica las credenciales y genera un token JWT con duración de 1 minuto.
*   `me`: Endpoint protegido. Devuelve datos del usuario actual (e imagen si existe).

## 5. Flujo de Autenticación

1.  El usuario envía sus credenciales al endpoint `/login/`.
2.  Se verifican las credenciales (comparando la contraseña encriptada con bcrypt).
3.  Si son correctas, se genera un token JWT con expiración de 1 minuto.
4.  El usuario incluye el token JWT en la cabecera `Authorization` para acceder a endpoints protegidos (como `/me/`).

## 6. Recursos Estáticos

*   La API sirve archivos estáticos desde el directorio `sources` (imágenes de usuario).

En resumen, este código implementa una API de autenticación segura con JWT, contraseñas encriptadas y protección de recursos.
