from fastapi import HTTPException, status
from sqlmodel import Session, select
from Models.models import User
from Utils.jwt import create_token

class AuthControll:

    def create_acess(full_name: str, email: str, passowrd: str, session: Session) -> dict:
        try:
            existing_user = session.exec(select(User).where(User.email == email)).first()

            if existing_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User existing")
            
            new_user = User(
                full_name=full_name,
                email=email,
                password=passowrd
            )

            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            return {
                "id": new_user.id,
                "full_name": new_user.full_name,
                "email": new_user.email
            }
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Bad Request: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {e}")
        
    def login_user(email: str, password, session: Session) -> dict:
        try:
            user = session.exec(select(User).where(User.email == email)).first()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user")
            
            if not user.check_password(password):
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid password")
            
            acess_token = create_token({'sub': user.id, "email": user.email})

            return {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "acess_token": acess_token
            }
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Bad Request: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {e}")