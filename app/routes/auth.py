# app/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from app.database.connection import get_db
from app.models.models import Usuario
from app.schemas.schemas import UsuarioCreate, UsuarioResponse, Token

# Clave secreta 
SECRET_KEY = "clave-secreta-peluqueria-2024"
ALGORITHM = "HS256"

# El token expira en 60 minutos
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# bcrypt es el algoritmo que encripta las contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Le dice a FastAPI dónde está el endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/auth", tags=["Autenticación"])

def encriptar_password(password: str) -> str:
    """Convierte la contraseña en un hash seguro."""
    return pwd_context.hash(password)

def verificar_password(password: str, hash: str) -> bool:
    """Compara la contraseña ingresada con el hash guardado."""
    return pwd_context.verify(password, hash)

def crear_token(data: dict) -> str:
    """Genera un token JWT con los datos del usuario."""
    datos = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos.update({"exp": expiracion})
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

def get_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Valida el token JWT y devuelve el usuario logueado.
    Se usa como dependencia en los endpoints protegidos.
    """
    credenciales_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credenciales_error
    except JWTError:
        raise credenciales_error

    # Busca el usuario en la BD
    usuario = db.query(Usuario).filter(Usuario.username == username).first()
    if usuario is None:
        raise credenciales_error
    return usuario

@router.post("/registro", response_model=UsuarioResponse, status_code=201)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario en el sistema."""
    existe = db.query(Usuario).filter(Usuario.username == usuario.username).first()
    if existe:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    nuevo_usuario = Usuario(
        username=usuario.username,
        password=encriptar_password(usuario.password)  # Nunca se guarda en texto plano
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Valida las credenciales y devuelve un token JWT."""
    usuario = db.query(Usuario).filter(Usuario.username == form_data.username).first()

    if not usuario or not verificar_password(form_data.password, usuario.password):
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    token = crear_token(data={"sub": usuario.username})
    return {"access_token": token, "token_type": "bearer"}