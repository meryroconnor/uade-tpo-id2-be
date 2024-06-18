from pydantic import BaseModel, Field, EmailStr

class SignUpDto(BaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    roles_id: int = Field(...)
    nickname: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "firstname": "Pepe",
                "lastname": "Argento",
                "email": "email@domain.com",
                "password": "weakpassword",
                "roles_id": "1",
                "nickname": "pep",
            }
        }

class LoginDto(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "email@domain.com",
                "password": "password"
            }
        }
