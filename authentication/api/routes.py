from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
import uuid

from authentication.domain.user import User, create_user, authenticate_user
from authentication.dependency_injection.di import redis_service

router = APIRouter(prefix="/auth", tags=["authentication"])

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(request: RegisterRequest):
    user = User(email=request.email, password=request.password)
    if create_user(user) is None:
        raise HTTPException(status_code=409, detail="El usuario ya existe")
    return {"message": "Usuario creado correctamente"}

@router.post("/login")
def login(request: LoginRequest):
    user = authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = str(uuid.uuid4())
    redis_service.set_token(token, user.email)
    return {"token": token}

@router.post("/logout")
def logout(Auth: str = Header(...)):
    deleted = redis_service.delete_token(Auth)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return {"message": "Sesión cerrada correctamente"}

@router.get("/introspect")
def introspect(Auth: str = Header(...)):
    user_email = redis_service.get_user_id(Auth)
    if not user_email:
        raise HTTPException(status_code=401, detail="Token inválido")
    return {"user": user_email}
