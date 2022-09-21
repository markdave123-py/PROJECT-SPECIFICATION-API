from typing import List
from ..database import  get_db
from .. import models,schemas,utils
from fastapi import status,Depends,APIRouter
from sqlalchemy.orm import Session

from .. import autho2


router = APIRouter(prefix='/auth',
                    tags=['create_user'])


@router.post('/users', status_code= status.HTTP_201_CREATED, response_model= schemas.Create_user_response)
def create_user(user: schemas.Create_user_request, db:Session = Depends(get_db)):
    user.password = utils.hash_password(user.password)
    message = "user sucessfully created!!"

    new_user = models.User(**user.dict())

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "Data": new_user,
        "Message": message
        }

@router.get("/users", response_model= List[schemas.User_response])
def get_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users


