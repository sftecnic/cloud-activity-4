from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str  # En producción, usar hashing

# Base de datos en memoria para usuarios (sólo para demo)
users_db = {}

def create_user(user: User) -> Optional[User]:
    if user.email in users_db:
        return None
    users_db[user.email] = user
    return user

def authenticate_user(email: str, password: str) -> Optional[User]:
    user = users_db.get(email)
    if user and user.password == password:
        return user
    return None
