import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate


def list_roles(db: Session) -> list[Role]:
    return list(db.execute(select(Role).order_by(Role.name)).scalars())


def get_role(db: Session, role_id: uuid.UUID) -> Role | None:
    return db.get(Role, role_id)


def get_by_name(db: Session, name: str) -> Role | None:
    return db.execute(select(Role).where(Role.name == name)).scalar_one_or_none()


def create_role(db: Session, data: RoleCreate) -> Role:
    role = Role(name=data.name, description=data.description)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def update_role(db: Session, role: Role, data: RoleUpdate) -> Role:
    patch = data.model_dump(exclude_unset=True)
    for k, v in patch.items():
        setattr(role, k, v)
    db.commit()
    db.refresh(role)
    return role


def delete_role(db: Session, role: Role) -> None:
    db.delete(role)
    db.commit()
