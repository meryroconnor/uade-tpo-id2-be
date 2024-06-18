from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

def generate_uuid():
    return str(uuid4())


class ProfileDto(BaseModel):
    user_id: str
    user_name: str
    description: str
    availability: int
    image: str
    birth_date: str 