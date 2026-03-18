from fastapi import FastAPI
from app.database.connection import engine, Base
from app.routes import auth, clientes, turnos

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Peluquería 💈",
    description="Sistema de gestión de turnos para peluquería con autenticación JWT",
    version="2.0.0"
)

app.include_router(auth.router)
app.include_router(clientes.router)
app.include_router(turnos.router)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de la Peluquería 💈"}