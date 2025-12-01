from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserOut
from app.utils import hash

router = APIRouter(prefix="/users", tags=["Users"])


# create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_users(user: UserCreate, db: Session = Depends(get_db)):
    # has the password- user.password
    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# get single user
@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} does not exist",
        )
    return user
