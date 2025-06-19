from datetime import timedelta, datetime, timezone
from typing import Annotated, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from dotenv import load_dotenv
import os
from app.pyapi.models.models import User
from app.pyapi.deps import db_dependency, bcrypt_context
from uuid import uuid4
import hashlib
from app.pyapi.database import create_supabase_client
supabase = create_supabase_client()

load_dotenv()

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")

class UserCreateRequest(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@auth_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: UserCreateRequest):
    create_user_model = User(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password)
    )
    db.add(create_user_model)
    db.commit()

@auth_router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    
    return {'access_token': token, 'token_type': 'bearer'}

@auth_router.post("/signup", response_model=User)
def signup(request: SignupRequest):
    # Check if user already exists
    existing = supabase.table("users").select("id").eq("email", request.email).execute()
    if existing.data and len(existing.data) > 0:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = str(uuid4())
    hashed_pw = hash_password(request.password)
    user_dict = {
        "id": user_id,
        "name": request.name,
        "email": request.email,
        "password": hashed_pw,
    }
    res = supabase.table("users").insert(user_dict).execute()
    if res.error:
        raise HTTPException(status_code=500, detail="Failed to create user")
    return User(**user_dict)

@auth_router.post("/login", response_model=User)
def login(request: LoginRequest):
    hashed_pw = hash_password(request.password)
    res = supabase.table("users").select("*").eq("email", request.email).eq("password", hashed_pw).single().execute()
    if res.error or not res.data:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return User(**res.data)
