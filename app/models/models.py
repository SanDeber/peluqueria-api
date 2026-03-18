from sqlalchemy import Column, Integer, String, Date
from app.database.connection import Base


class Usuario(Base):
    """Representa al dueño o empleado que usa el sistema."""
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Se guarda encriptada


class Cliente(Base):
    """Representa a los clientes de la peluquería."""
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


class Turno(Base):
    """Representa un turno reservado."""
    __tablename__ = "turnos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(String, nullable=False)
    estado = Column(String, default="activo")
