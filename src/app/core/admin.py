from fastapi import Depends, HTTPException, status
from app.core.deps import get_current_user
from app.models.user import User


def require_admin(user: User = Depends(get_current_user)) -> User:
    if not getattr(user, "is_superuser", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user
