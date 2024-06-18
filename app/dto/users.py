from pydantic import BaseModel

class UsersDto(BaseModel):
    id: int
    firstname: str
    lastname: str
    password: str
    roles_id: int
    nickname: str