# app/schemas/schemas.py

from pydantic import BaseModel
from datetime import date
from typing import Literal

class UsuarioCreate(BaseModel):
    username: str
    password: str

class UsuarioResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ClienteCreate(BaseModel):
    nombre: str
    telefono: str
    email: str

class ClienteResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str

    class Config:
        from_attributes = True

class TurnoCreate(BaseModel):
    cliente_id: int
    fecha: date        # Formato: "2024-12-25"
    hora: str          # Formato: "10:30"

class TurnoResponse(BaseModel):
    id: int
    cliente_id: int
    fecha: date
    hora: str
    estado: Literal["activo", "cancelado"]

    class Config:
        from_attributes = True