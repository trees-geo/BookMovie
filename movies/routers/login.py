from fastapi import APIRouter, status, HTTPException
from .. import schemas, models
from ..database import get_database_session
from passlib.context import CryptContext
from fastapi.params import Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token:str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid auth credentials"
    )
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("user")
        if not username:
            raise credentials_exception
        token_data = schemas.TokenUser(username=username)
        return token_data
    except JWTError:
        raise credentials_exception

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "602f625a03237d3c9d6baa7db0416a14de0dea17c56acfd78add111d6b6cfcc1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": expire.isoformat()})
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
    return {"access_token": access_token, "token_type": "bearer"}
