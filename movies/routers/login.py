from fastapi import APIRouter, status, HTTPException
from .. import schemas, models
from ..database import get_database_session
from passlib.context import CryptContext
from fastapi.params import Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import time

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token:str = Depends(oauth_scheme)):
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid auth credentials"
    )
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM, options={"verify_exp": True})
        username: str = payload.get("user")
        if not username:
            raise credentials_exception
        token_data = schemas.TokenUser(username=username)
        return token_data
    except ExpiredSignatureError as e:
        print(e)
        print("Redirect to login")
        raise credentials_exception
    except JWTError as e:
        raise credentials_exception

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "602f625a03237d3c9d6baa7db0416a14de0dea17c56acfd78add111d6b6cfcc1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_MINUTES = 2

def generate_token(data: dict, refresh=False):
    TOKEN_EXPIRY = ACCESS_TOKEN_EXPIRE_MINUTES * 60 if not refresh else REFRESH_TOKEN_EXPIRE_MINUTES * 60
    to_encode = data.copy()
    to_encode.update({
        "iat": int(time.time()),
        "exp": int(time.time()) + TOKEN_EXPIRY
    })
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

router = APIRouter(tags=["Login"])

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_database_session)):
    user = db.query(models.Producer).filter(models.Producer.name == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid User. Please Sign up")
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=404, detail="Invalid Password. Please Retry")
    access_token = generate_token({"user": user.name})
    refresh_token = generate_token({"user": user.name}, True)
    new_user = models.User(username=user.name, refresh_token=refresh_token)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/refresh")
def get_new_access_token(request: schemas.TokenUser, db: Session = Depends(get_database_session)):
    refresh_token = request.refresh_token
    try:
        payload = jwt.decode(refresh_token, key=SECRET_KEY, algorithms=ALGORITHM, options={"verify_exp": True})
        access_token = generate_token({"user": payload.get("user")})
        return {"access_token": access_token, "refresh_token": refresh_token}
    except ExpiredSignatureError:
        print("refresh_token expired")
        payload = jwt.decode(refresh_token, key=SECRET_KEY, algorithms=ALGORITHM, options={"verify_exp": False})
        db.query(models.User).filter(models.User.username == payload.get("user")).update({models.User.refresh_token == ""})
        raise HTTPException(status_code=404, detail="Invalid Token. Please Login")
        

