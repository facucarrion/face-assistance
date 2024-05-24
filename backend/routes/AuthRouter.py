from fastapi import APIRouter
from schemas.AuthSchema import LoginSchema

auth_router = APIRouter(
    prefix="/auth",
)

@auth_router.post("/login")
async def login(user: LoginSchema):
    return user