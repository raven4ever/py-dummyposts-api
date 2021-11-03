from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, utils, oauth2, schemas
from ..database import get_db

router = APIRouter(tags=['Auth'])


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usr = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not usr:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid credentials!')

    if not utils.verify_password(user_credentials.password, usr.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid credentials!')

    access_token = oauth2.create_access_token(data={"user_id": usr.id})

    return {"access_token": access_token, "token_type": "bearer"}
