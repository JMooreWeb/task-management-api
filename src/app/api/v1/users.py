from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.schemas.user import UserOut
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserOut, description="Get the current authenticated user's profile information.")
def me(user: User = Depends(get_current_user)):
    return user
