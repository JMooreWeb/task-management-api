import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole


def list_roles_for_user(db: Session, user_id: uuid.UUID) -> list[Role]:
    user = db.get(User, user_id)
    return user.roles if user else []


def assign_role(db: Session, user_id: uuid.UUID, role_id: uuid.UUID) -> UserRole:
    # Ensure both exist
    if not db.get(User, user_id):
        raise ValueError("user_not_found")
    if not db.get(Role, role_id):
        raise ValueError("role_not_found")

    existing = db.get(UserRole, {"user_id": user_id, "role_id": role_id})
    if existing:
        return existing

    link = UserRole(user_id=user_id, role_id=role_id)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def remove_role(db: Session, user_id: uuid.UUID, role_id: uuid.UUID) -> None:
    link = db.get(UserRole, {"user_id": user_id, "role_id": role_id})
    if link:
        db.delete(link)
        db.commit()


def list_users_for_role(db: Session, role_id: uuid.UUID) -> list[User]:
    role = db.get(Role, role_id)
    return role.users if role else []
