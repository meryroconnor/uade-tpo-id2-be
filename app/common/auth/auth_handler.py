import time
from typing import Dict

import jwt
from decouple import config

JWT_SECRET = config("JWT_SECRET")
JWT_EXP_MINUTES = int(config("JWT_EXP_MINUTES"))

def sign_jwt(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 60 * JWT_EXP_MINUTES
    }
    token = jwt.encode(payload, JWT_SECRET)
    return {
        "access_token": token
    }

def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=["HS256"])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
