from fastapi import Depends
from decouple import config
from jwt import decode
from .auth_bearer import JWTBearer

JWT_SECRET = config("JWT_SECRET")

async def get_current_user(token = Depends(JWTBearer())) -> dict:
    payload = decode(token, JWT_SECRET, algorithms=["HS256"], verify_signature=False)
    return {
        "email": payload.get("user_id")
    }
