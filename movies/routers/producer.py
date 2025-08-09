from fastapi import APIRouter
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from .. import schemas
from .. import models
from ..database import get_database_session
from fastapi.params import Depends
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=['Producer'])

@router.post("/addproducer", response_model=schemas.ProducerResponse)
def add_producer(request: schemas.Producer, db: Session = Depends(get_database_session)):
    hashed_pwd = pwd_context.hash(request.password)
    new_producer = models.Producer(name=request.name, email=request.email, password=hashed_pwd)
    db.add(new_producer)
    db.commit()
    db.refresh(new_producer)
    return JSONResponse(
        status_code=201,
        content="Producer added successfully"
    )