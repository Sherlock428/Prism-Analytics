from fastapi import APIRouter, Depends, status
from Controllers.auth_controller import AuthControll
from Models.schemas import UserCreate, UserRead, AuthPublic, AuthUser
from Database.db import get_session
from sqlmodel import Session

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(dados: UserCreate, session: Session = Depends(get_session)):
    
    new_user = AuthControll.create_acess(dados.full_name, dados.email, dados.password, session)

    return new_user

@router.post("/login", response_model=AuthPublic, status_code=status.HTTP_200_OK)
def login(dados: AuthUser, session: Session = Depends(get_session)):
    
    user = AuthControll.login_user(email=dados.email, password=dados.password, session=session)

    return user