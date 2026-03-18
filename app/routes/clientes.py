from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.models import Cliente, Usuario
from app.schemas.schemas import ClienteCreate, ClienteResponse
from app.routes.auth import get_usuario_actual

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=ClienteResponse, status_code=201)
def crear_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_usuario_actual)  
):
    """Crea un nuevo cliente. Requiere estar autenticado."""
    existe = db.query(Cliente).filter(Cliente.email == cliente.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    nuevo_cliente = Cliente(
        nombre=cliente.nombre,
        telefono=cliente.telefono,
        email=cliente.email
    )
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

@router.get("/", response_model=list[ClienteResponse])
def listar_clientes(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_usuario_actual)  # 🔒 Requiere login
):
    """Lista todos los clientes. Requiere estar autenticado."""
    return db.query(Cliente).all()