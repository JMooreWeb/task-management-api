from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.security import verify_password, create_access_token
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import Token

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=201, description="Register a new user by providing email, username, password, and optional profile information.")
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if crud_user.get_by_email(db, payload.email) or crud_user.get_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="Email or username already exists")
    return crud_user.create(db, payload)

@router.post("/token", response_model=Token, description="Obtain an access token by providing username/email and password.")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm uses: username + password (we accept username OR email in username field)
    u = crud_user.get_by_username(db, form.username) or crud_user.get_by_email(db, form.username)
    if not u or not verify_password(form.password, u.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=str(u.id))
    return Token(access_token=token)
