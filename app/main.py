# app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

# Importar y añadir los routers de autenticación y archivos
from authentication.api.routes import router as auth_router
from files.api.routes import router as files_router

app.include_router(auth_router)
app.include_router(files_router)
