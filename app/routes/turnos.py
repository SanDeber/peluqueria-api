from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.models import Turno, Cliente, Usuario
from app.schemas.schemas import TurnoCreate, TurnoResponse
from app.routes.auth import get_usuario_actual

router = APIRouter(prefix="/turnos", tags=["Turnos"])

@router.post("/", response_model=TurnoResponse, status_code=201)
def crear_turno(
    turno: TurnoCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_usuario_actual)  # 🔒 Requiere login
):
    """Crea un turno validando que el cliente exista y no haya doble reserva."""

    # 1. Verificar que el cliente existe
    cliente = db.query(Cliente).filter(Cliente.id == turno.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # 2. Evitar doble reserva en la misma fecha y hora
    doble_reserva = db.query(Turno).filter(
        Turno.fecha == turno.fecha,
        Turno.hora == turno.hora,
        Turno.estado == "activo"
    ).first()
    if doble_reserva:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un turno activo el {turno.fecha} a las {turno.hora}"
        )

    # 3. Crear el turno
    nuevo_turno = Turno(
        cliente_id=turno.cliente_id,
        fecha=turno.fecha,
        hora=turno.hora,
        estado="activo"
    )
    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)
    return nuevo_turno


@router.get("/", response_model=list[TurnoResponse])
def listar_turnos(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_usuario_actual)  # 🔒 Requiere login
):
    """Lista todos los turnos. Requiere estar autenticado."""
    return db.query(Turno).all()


@router.patch("/{turno_id}/cancelar", response_model=TurnoResponse)
def cancelar_turno(
    turno_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_usuario_actual)  # 🔒 Requiere login
):
    """Cancela un turno. Requiere estar autenticado."""
    turno = db.query(Turno).filter(Turno.id == turno_id).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    if turno.estado == "cancelado":
        raise HTTPException(status_code=400, detail="El turno ya está cancelado")

    turno.estado = "cancelado"
    db.commit()
    db.refresh(turno)
    return turno