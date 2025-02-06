# Instalamos libreria de criptografía para encriptar token
# pip install "python-jose[cryptography]"

# Instalamos libreria que contiene el algoritmo de encriptación
# pip install "passlib[bcrypt]"

# Importamos el framework fastapi a nuestro entorno de trabajo
from fastapi import FastAPI, Depends, HTTPException, status
# Importamos pydantic para obtener una entidad que pueda definir usuarios
from pydantic import BaseModel


from fastapi.responses import FileResponse

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# Importamos librería jwt
from jose import jwt, JWTError
# Importamos libreria passlib (algoritmo de encriptación)
from passlib.context import CryptContext
# Importamos libreria de fechas para la expiración del token
from datetime import datetime, timedelta
# Importamos la clase staticfiles para recursos estáticos****
from fastapi.staticfiles import StaticFiles

# Implementamos algoritmo de haseo para encriptar contraseña
ALGORITHM = "HS256"
# Duración de autenticación
ACCESS_TOKEN_DURATION = 1
# Creamos un secret
SECRET = "123456789"

# Creamos un objeto o instancia a partir de la clase FastAPI
app = FastAPI()


# Creamos una app para acceder al directorio de recursos estaticos***
app.mount("/sources", StaticFiles(directory="sources"), name="sources")

# Autenticación por contraseña para eso:
# Creamos un endpoint llamado "login"
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Creamos contexto de encriptación para eso importamos libreria passlib y elegimos algoritmo de incriptación "bcrypt"
# Utilizamos bcrypt generator para encriptar nuestras contraseñas
crypt = CryptContext(schemes="bcrypt")

# generamos la contraseña encriptada para guardarla en base de datos
# https://bcrypt-generator.com/4


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class equipo(BaseModel):
    username: str
    disabled: bool
# Definimos la clase para el usuario de base de datos


class UserDB(User):
    password: str

users_db = {
    "David": {
        "username": "David",
        "full_name": "BLAS BRAVO DAVID",
        "email": "david.blasb@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$ETvgQxpojKqoBjT0oU1ITeZp85sYhbdf6pkvyMIyucAk4V/q4VgJe"
    },
    "Javier": {
        "username": "Javier",
        "full_name": "CORDERO TEAPILA ALDO JAVIER",
        "email": "aldo.cordero@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$TH1GKt8AsbOyJm99GEE0kuBotk9SekKNuhqvqaam4P91ibpkPRMWm"
    },
    "Gerardo": {
        "username": "Gerardo",
        "full_name": "CRUZ SOSA LUIS GERARDO",
        "email": "luis.cruzso@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$xVv0jH39xTsuDzMwK6FF9eyYztr2oNG/6f30GpZqQznFHjtwsTIjq"
    },
    "Susana": {
        "username": "Susana",
        "full_name": "GOMEZ CHAVEZ KARYME SUSANA",
        "email": "karyme.gomez@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$/Gcx8tp2SiICRnThQDwcWeJ1A/BI7pVfIjYJMAsBJjGvcdZqghMKS"
    },
    "Luis": {
        "username": "Luis",
        "full_name": "GONZALEZ AVENDANO LUIS DAVID",
        "email": "luis.gonzalezav@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$ilyG9Nbxf6QELEY3toaq6uFAewNFKVYJjB3UCKv3/OQEfj0MA2Xgi"
    },
    "Hugo": {
        "username": "Hugo",
        "full_name": "GORGONIO HERNANDEZ HUGO",
        "email": "hugo.gorgonio@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$BGhupnfW7U40yKd/01tA2.wGdo/R9dlhM3Ly3uzx5qfDeq8PWoG/W",
    },
    "Diego": {
        "username": "Diego",
        "full_name": "GUTIERREZ BARRANCO LUIS DIEGO",
        "email": "luis.gutierrezba@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$izLu7CE8O4/QGBYhATab0e9I4TbpfDq7Rpdj4lmHKa9RYt4CED.PW",
    },
    "Victor": {
        "username": "Victor",
        "full_name": "GUTIERREZ FLORES VICTOR MANUEL",
        "email": "victor.gutierrezf@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$c2MLsCcnZJOTO3kUtAfEze//A0/gYyUaroLYE.capaJ0AUJjQuUNO",
    },
    "Fernando": {
        "username": "Fernando",
        "full_name": "HERRERA RAMIREZ EDGAR FERNANDO",
        "email": "edgar.herrerar@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$F1w0C4FptFl8QJKgHykYLOTqQDcJJNwLcGMIn9tx.hQbuh/icp3yK",
    },
    "Yasser": {
        "username": "Yasser",
        "full_name": "LANDA ARGUELLO ARMANDO YASSER",
        "email": "armando.landa@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$l6O7FMyo4SYtyR73Y3Ws6uPBJloweXFVd/sxFlMx99oGoXAzyOwUy",
    },
    "Angelica": {
        "username": "Angelica",
        "full_name": "LANDETA CALVARIO NORMA ANGELICA",
        "email": "norma.landeta@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$fNWE7XDTi.otV9MuIUwKhu.VePJqInx4SGNdQPqp/bdRON1ZdH5Uu",
    },
    "Carmen": {
        "username": "Carmen",
        "full_name": "LIMON GARCIA MARIA DEL CARMEN",
        "email": "maria.limongar@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$sQ6ATwN8JgTWCx3DkULU1el.hSOFtFQcUK05Wg.TTCRa5VzS3QLq.",
    },
    "Jafet": {
        "username": "Jafet",
        "full_name": "MARAVILLA LOPEZ JAFET",
        "email": "jafet.maravilla@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$1ESFJZr2UneRHVxeVBCBaeRoqvKBnDVoMV/tdhGy4hufcCNsQAOuq",
    },
    "Miguel": {
        "username": "Miguel",
        "full_name": "MARIE SANCHEZ MIGUEL ANGEL",
        "email": "miguel.marie@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$rtr/F69ZPdMaSFb4.ZbzDOUZpjDpNvNSvyPbn7e70lm4R2.I1HtAW"
    },
    "Arturo": {
        "username": "Arturo",
        "full_name": "MARRUFO POLANCO RICARDO ARTURO",
        "email": "ricardo.marrufop@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$TB4omemDE6YJMGXiIOfOd.0ZSNWGGZ3yEm/IbFfomsS9JamHoIVm."
    },
    "Eunice": {
        "username": "Eunice",
        "full_name": "MARTINEZ BARRALES EUNICE",
        "email": "eunice.martinezb@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$/e8OV/WHwyhj767lzw48peAEosn8dRGayZGA4dLPm1WEcBx0Jjqie"
    },
    "Jonathan": {
        "username": "Jonathan",
        "full_name": "PEREZ BALCON ABDIEL JONATHAN",
        "email": "abdiel.perezb@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$3ZhIjnk43HyvIdCFfGYtJODlUzHqzx5OB8HMxYwSSMjbmAxUBC7rm"
    },
    "Jordy": {
        "username": "Jordy",
        "full_name": "RAMIREZ HERNANDEZ JORDY",
        "email": "jordy.ramirez@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$tMPKrqC6n4xubobtCYbeaOKB8VK56Rx5mutBPa5Iv0d62WI8VmOzW"
    },
    "Rodrigo": {
        "username": "Rodrigo",
        "full_name": "SANTOS DE JESUS RODRIGO",
        "email": "rodrigo.santosdej@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$oPoykh3usCP88ScvrIWRTOLvky4k2FOWm4u4DYqEi86Y1KLoX68Bm"
    },
    "Noe": {
        "username": "Noe",
        "full_name": "SEDANO JIMENEZ LEONARDO NOE",
        "email": "leonardo.sedanoji@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$koShOmwAJzAIiA5CPVw4lOKwZeggZe/fjXftZ8vbsG1ZFTT/Ar6f6"
    },
    "Tania": {
        "username": "Tania",
        "full_name": "SEVILLA JIMENEZ TANIA",
        "email": "tania.sevilla@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$J8dd8CcciEgTh57eznjTXeqRpo00V9WTKdSvnY9cksoIV4mHVUto6"
    },
    "Ivan": {
        "username": "Ivan",
        "full_name": "SOLANO CARRERA IVAN",
        "email": "ivan.solano@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$4k81OTVmekPFruPNmxJMR.DaoCofinmqIGYR9KhOzK6MjTvIS.Ma."
    },
    "Eduardo": {
        "username": "Eduardo",
        "full_name": "SUAREZ SALVATIERRA ANGEL EDUARDO",
        "email": "angel.suarezsa@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$Wa11m./YbdvthwEwCCC7HuUMWsbpdOFhI0Z44tQv/p3VGUwY64U.u"
    },
    "Jesus": {
        "username": "Jesus",
        "full_name": "TLAMANI XOCHIMITL JESUS",
        "email": "jesus.tlamani@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$oONrILqWLQx4KgTRgL2eYeagcJEMMpuPahOOlPYD22qMf51u7Ecyq"
    },
    "Freddy": {
        "username": "Freddy",
        "full_name": "Freddy García",
        "email": "alfredo.garcias@alumno.buap.mx",
        "disabled": False,
        "password": "$2a$12$Px4/G9Onxs4m6QxjAwsbtOmqf4BFxkLUvn3F5PFPbWmhWLYEyGObG"  # "1234"
    }
}


# 1 Función para regresar el usuario completo de la base de datos (users_db), con contraseña encriptada
def search_user_db(username: str):
    if username in users_db:
        # ** devuelve todos los parámetros del usuario que coincida con username
        return UserDB(**users_db[username])

# 4 Función final para devolver usuario a la solicitud del backend


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

# Funcion para devolver recurso estatico dependiendo del usuario


    # 3 Esta es la dependencia para buscar al usuario


async def auth_user(token: str = Depends(oauth2)):
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Credenciales de autenticación inválidas")

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credenciales de autenticación inválidas")
    return search_user(username)

# 2 Función para determinar si usuario esta inactivo


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user


@app.post("/login/")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Busca en la base de datos "users_db" el username que se ingreso en la forma
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    # Se obtienen los atributos incluyendo password del usuario que coincida el username de la forma
    user = search_user_db(form.username)

    # user.password es la contraseña encriptada en la base de datos
    # form.password es la contraseña original que viene en formulario
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="La contraseña no es correcta")
    # Creamos expiración de 1 min a partir de la hora actual
    access_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION)
    # Tiempo de expiración: hora actual mas 1 minuto
    expire = datetime.utcnow()+access_token_expiration

    access_token = {"sub": user.username, "exp": expire}
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@app.get("/me/")
# Crea un user de tipo User que depende de la función (current_user)
async def me(user: User = Depends(current_user)):
    username = user.username
    if username in users_db:
        url = "sources/"+username+".png"
        return FileResponse(url)
    return user

# http://127.0.0.1:8000/login/

# username:Freddy
# password:1234

# http://127.0.0.1:8000/me/

# -uvicorn 7_jwt_auth_users:app --reload
