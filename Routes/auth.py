from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"])

@router.post("/register")
def register():
    pass

@router.post("/login")
def login():
    pass