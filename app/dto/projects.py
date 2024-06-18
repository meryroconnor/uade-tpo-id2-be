from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

def generate_uuid():
    return str(uuid4())

def generate_date():
    return str(datetime.now())

class ProjectDto(BaseModel):
    project_id: str
    title: str
    description: str
    creation_date: str = Field(default_factory=generate_date)
    due_date: str
    
