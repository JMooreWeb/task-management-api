import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.admin import require_admin
from app.schemas.role import RoleCreate, RoleUpdate, RoleOut
from app.crud import role as crud_role

router = APIRouter()


@router.get("/", response_model=list[RoleOut], description="Retrieve a list of all roles in the system.")
def list_roles(db: Session = Depends(get_db)):
    return crud_role.list_roles(db)


@router.get("/{role_id}", response_model=RoleOut, description="Retrieve a specific role by its ID.")
def get_role(role_id: uuid.UUID, db: Session = Depends(get_db)):
    role = crud_role.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.post("/", response_model=RoleOut, status_code=status.HTTP_201_CREATED, description="Create a new role.")
def create_role(payload: RoleCreate, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    if crud_role.get_by_name(db, payload.name):
        raise HTTPException(status_code=400, detail="Role already exists")
    return crud_role.create_role(db, payload)


@router.patch("/{role_id}", response_model=RoleOut, description="Update a specific role by its ID.")
def update_role(role_id: uuid.UUID, payload: RoleUpdate, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    role = crud_role.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if payload.name and payload.name != role.name and crud_role.get_by_name(db, payload.name):
        raise HTTPException(status_code=400, detail="Role name already exists")
    return crud_role.update_role(db, role, payload)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a specific role by its ID.")
def delete_role(role_id: uuid.UUID, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    role = crud_role.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    crud_role.delete_role(db, role)
    return None
