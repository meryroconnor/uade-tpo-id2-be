from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

def generate_uuid():
    return str(uuid4())

def generate_date():
    return str(datetime.now())

class TasksDto(BaseModel):
    task_id: str
    title: str
    description: str
    duration: int
    status: str 