from lib2to3.pgen2.token import tok_name
from .. import autho2,utils,models,database
from fastapi import APIRouter, Depends,status,Response,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

router = APIRouter(tags=["Authentication"])

@router.post('/auth/users/login',status_code=status.HTTP_201_CREATED)
def login_user(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not utils.verify(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = autho2.create_token(data={'user_id': user.id})

    return {
        "message": "Token successfully created you can login in",
        'token': access_token,
        'token_type': "bearer"
    }