# routes/auth_routes.py
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse
from app.pyapi.database import get_supabase
from fastapi.templating import Jinja2Templates
from starlette.responses import Response, RedirectResponse
from pydantic import BaseModel
from app.pyapi.deps import bcrypt_context
from app.pyapi.models.models import User
from datetime import timedelta, datetime, timezone
from jose import jwt
from dotenv import load_dotenv
import os
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
load_dotenv()

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
class UserCreateRequest(BaseModel):
    email: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
supabase=get_supabase()

def authenticate_user(email: str, password: str):
    response = supabase.table("user").select("*").eq("email", email).execute()
    if not response:
        return False
    if not password==response.data[0]["password"]:
        return False
    return response

def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': email, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/signup")
async def signup(create_user_request: UserCreateRequest):
    try:
        supabase.table("user").insert({
            'email': create_user_request.email,
            'password': create_user_request.password
        }).execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    router.get("/")

@router.post("/login")
async def login(response: Response, email: str = Form(...), password: str = Form(...)):
    try:
        user=authenticate_user(email, password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        router.get("/")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                ):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user.data[0]["email"], user.data[0]["id"], timedelta(minutes=60))
    
    return {'access_token': token, 'token_type': 'bearer'}
