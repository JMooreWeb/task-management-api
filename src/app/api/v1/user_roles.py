import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.core.admin import require_admin
from app.models.user import User
from app.schemas.role import RoleOut
from app.schemas.user_role import AssignRoleIn, UserRoleOut
from app.crud import user_role as crud_user_role

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me/roles", response_model=list[RoleOut], description="List all roles assigned to the current user.")
def my_roles(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return crud_user_role.list_roles_for_user(db, user.id)


@router.get("/{user_id}/roles", response_model=list[RoleOut], description="List all roles assigned to a specific user.")
def list_roles_for_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    return crud_user_role.list_roles_for_user(db, user_id)


@router.post("/{user_id}/roles", response_model=UserRoleOut, status_code=status.HTTP_201_CREATED, description="Assign a role to a specific user.")
def assign_role_to_user(
    user_id: uuid.UUID,
    payload: AssignRoleIn,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    try:
        link = crud_user_role.assign_role(db, user_id=user_id, role_id=payload.role_id)
        return link
    except ValueError as e:
        if str(e) == "user_not_found":
            raise HTTPException(status_code=404, detail="User not found")
        if str(e) == "role_not_found":
            raise HTTPException(status_code=404, detail="Role not found")
        raise


@router.delete("/{user_id}/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT, description="Remove a role from a specific user.")
def remove_role_from_user(
    user_id: uuid.UUID,
    role_id: uuid.UUID,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    crud_user_role.remove_role(db, user_id=user_id, role_id=role_id)
    return None
