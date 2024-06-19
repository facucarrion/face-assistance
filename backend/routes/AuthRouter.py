from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.AuthSchema import LoginSchema, RegisterSchema
from schemas.ApiMessages import ApiMessageSchema
from config.database import get_db
from lib.auth.crud import get_user_by_username
from lib.auth.password import hash_password, verify_password
from lib.auth.token import create_access_token

auth_router = APIRouter(
    prefix="/auth",
)

@auth_router.post("/homepage", response_model=ApiMessageSchema)
async def login(user: LoginSchema, db: Session = Depends(get_db)):
    userInDatabase = get_user_by_username(db, user.username)

    if userInDatabase is None:
        return {
            "success": False,
            "status": 401,
            "message": "User not found"
        }
    
    if not verify_password(user.password, userInDatabase.password):
        return {
            "success": False,
            "status": 401,
            "message": "Incorrect password"
        }
    
    user_dict = {
        "id_user": userInDatabase.id_user,
        "username": userInDatabase.username,
        "password": userInDatabase.password,
        "rol": userInDatabase.rol
    }

    return {
        "success": True,
        "status": 200,
        "message": "User logged in successfully",
        "data": {
            "id_user": user_dict["id_user"],
            "token": create_access_token(user_dict)
        }
    }

@auth_router.post("/register", response_model=ApiMessageSchema)
async def register(newUserData: RegisterSchema):
    return {
        "success": True,
        "status": 200,
        "message": "User registered successfully",
        "data": {
            "password": hash_password(newUserData.password)
        }
    }