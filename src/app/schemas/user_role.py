import uuid
from pydantic import BaseModel


class AssignRoleIn(BaseModel):
    role_id: uuid.UUID


class UserRoleOut(BaseModel):
    user_id: uuid.UUID
    role_id: uuid.UUID

    model_config = {"from_attributes": True}
