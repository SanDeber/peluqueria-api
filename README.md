# 💈 Peluquería API

API REST para la gestión de turnos de una peluquería, desarrollada con **Python** y **FastAPI**.

## Tecnologías utilizadas

- **Python 3.11**
- **FastAPI** — Framework web moderno y de alto rendimiento
- **SQLAlchemy** — ORM para manejo de base de datos
- **SQLite** — Base de datos liviana para desarrollo
- **JWT (JSON Web Tokens)** — Autenticación segura
- **Pydantic** — Validación de datos
- **Uvicorn** — Servidor ASGI

## Funcionalidades

- Registro y login de usuarios con JWT
- Endpoints protegidos por autenticación
- CRUD completo de clientes
- Creación y listado de turnos
- Cancelación de turnos
- Validación de doble reserva en la misma fecha y hora
- Documentación automática con Swagger UI

## Estructura del proyecto
```
peluqueria-api/
│
├── app/
│   ├── main.py              # Punto de entrada
│   ├── database/
│   │   └── connection.py    # Configuración de la BD
│   ├── models/
│   │   └── models.py        # Tablas de la base de datos
│   ├── schemas/
│   │   └── schemas.py       # Validación de datos
│   └── routes/
│       ├── auth.py          # Login y registro
│       ├── clientes.py      # Endpoints de clientes
│       └── turnos.py        # Endpoints de turnos
│
├── requirements.txt
└── README.md
```

## Instalación
```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/peluqueria-api.git
cd peluqueria-api

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Arrancar el servidor
uvicorn app.main:app --reload
```

## Documentación

Una vez corriendo el servidor, accedé a:

- Swagger UI → http://127.0.0.1:8000/docs
- ReDoc → http://127.0.0.1:8000/redoc

## Cómo usar la autenticación

1. Registrarse en `POST /auth/registro`
2. Loguearse en `POST /auth/login` para obtener el token
3. Hacer click en el botón **Authorize** en el Swagger
4. Pegar el token y ya podés usar todos los endpoints

## Endpoints principales

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/auth/registro` | Registrar usuario | No |
| POST | `/auth/login` | Iniciar sesión | No |
| POST | `/clientes` | Crear cliente | ✅ |
| GET | `/clientes` | Listar clientes | ✅ |
| POST | `/turnos` | Crear turno | ✅ |
| GET | `/turnos` | Listar turnos | ✅ |
| PATCH | `/turnos/{id}/cancelar` | Cancelar turno | ✅ |

## SanDeber

**Debernardi Santino**  
Estudiante de Programación — UTN  
[GitHub](https://github.com/SanDeber)
