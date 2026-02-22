from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.security import verify_password, create_access_token
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import Token


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=201, description="Register a new user by providing email, username, password, and optional profile information.")
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if crud_user.get_by_email(db, payload.email) or crud_user.get_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="Email or username already exists")
    return crud_user.create(db, payload)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_core(form_data, db)


@router.post("/token", response_model=Token, include_in_schema=False)
def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_core(form_data, db)


def login_core(form: OAuth2PasswordRequestForm, db: Session) -> Token:
    user = crud_user.get_by_username(db, form.username) or \
           crud_user.get_by_email(db, form.username)
        
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=str(user.id))
    return Token(access_token=token)
