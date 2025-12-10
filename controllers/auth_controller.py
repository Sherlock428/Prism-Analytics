from fastapi import HTTPException, status
from sqlmodel import Session, select
from Models.models import User
from Utils.jwt import create_token

class AuthControll:

    def create_acess(full_name: str, email: str, password: str, session: Session) -> dict:
        try:
            existing_user = session.exec(select(User).where(User.email == email)).first()

            if existing_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User já existe")
            
            new_user = User(
                full_name=full_name,
                email=email,
                password=password
            )

            new_user.set_password(password)
            
            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            return {
                "id": new_user.id,
                "full_name": new_user.full_name,
                "email": new_user.email
            }
        
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Error: {e}")
        
    def login_user(email: str, password: str, session: Session) -> dict:
        try:
            user = session.exec(select(User).where(User.email == email)).first()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user não encontrado")

            if not user.check_password(password):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or password invalids")
            
            token = create_token({"sub": user.id, "email": email})

            return {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "acess_token": token,
                "token_type": "bearer"
            } 
        
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Error: {e}")
        
    def profile(user_id: str, session: Session) -> dict:
        try:
            user = session.exec(select(User).where(User.id == user_id)).first()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found User")
            
            return {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
            }
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Error: {e}")
