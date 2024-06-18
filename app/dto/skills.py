from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

def generate_uuid():
    return str(uuid4())


class SkillDto(BaseModel):
    skill_id: str
    description: str