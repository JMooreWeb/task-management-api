import uuid
from pydantic import BaseModel, EmailStr
from app.schemas.role import RoleOut

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: str
    last_name: str
    phone_number: str | None = None
    is_active: bool = True
    is_verified: bool = False
    is_superuser: bool = False

class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    phone_number: str | None = None
    roles: list[RoleOut] = []
    
    model_config = {"from_attributes": True}
