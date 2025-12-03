from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from Models.models import User
from Database.db import get_session
from dotenv import load_dotenv
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITH")

oauth2_schema = OAuth2PasswordBearer("/auth/login")

def create_token(data: dict):
    encode_item = data.copy()
    encode_jwt = jwt.encode(encode_item, SECRET_KEY, ALGORITHM)

    return encode_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token)

        return payload
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token",
                            headers={"WWW-authenticate": "Bearer"})
    
async def current_user(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)) -> User:
    try:
        payload = verify_token(token)
        user_id = payload.get('sub')

        user = session.exec(select(User).where(User.id == user_id)).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found User")
        
        return user
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro: {e}")
    