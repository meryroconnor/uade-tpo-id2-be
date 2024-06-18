from fastapi import APIRouter, HTTPException, status

from app.dto.auth import SignUpDto, LoginDto
from .auth_service import signupService, loginService

router = APIRouter()
entity = "auth"

@router.post("/signup", tags=[entity])
async def signup(req: SignUpDto):
    try:
        return signupService(req)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@router.post("/login", tags=[entity])
async def login(req: LoginDto):
    try:
        return loginService(req)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
