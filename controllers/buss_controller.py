from fastapi import HTTPException, status
from sqlmodel import Session, select
from Utils.jwt import current_user

class BussControll:

    async def create_buss(name: str, email: str, logo_url: str, googles_maps: str, qr_code_url):
        pass

    async def get_buss():
        pass

    async def edit_buss():
        pass

    async def delete_buss():
        pass
    